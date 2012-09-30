__author__ = 'yablokoff'

from  copy import copy
import numpy
from scipy.sparse import lil_matrix
from dumb_perms import get_good_tables

N = 3

class TripleRow:
     def __init__(self, first, second, third):
         self.triple = [first, second, third]
         self.values = []

     def __str__(self):
         return repr(self.triple)

def generate_permutations_of_three(n):
    all_triples = []
    for i in range(1, n+1):
        for j in range(1, n+1):
            for k in range(1, n+1):
                all_triples.append(TripleRow(i, j, k))
    return all_triples

def generate_permutations_of_two(n):
    all_twos = []
    for i in range(1, n+1):
        for j in range(1, n+1):
            all_twos.append( (i,j) )
    return all_twos

def generate_op_matrix(triple, two, n):
    def set_value(posx, posy, val, matrix):
        pos = (posx-1, posy-1)
        if matrix[pos] != 0 and matrix[pos] != val:
            return False
        matrix[pos] = val
        return True

    matrix = numpy.zeros((n,n), dtype=int)
    if not set_value(triple.triple[0], triple.triple[1], two[0], matrix):
        return False
    if not set_value(triple.triple[1], triple.triple[2], two[1], matrix):
        return False
    third_step = (two[0]-1, triple.triple[2]-1)
    forth_step = (triple.triple[0]-1, two[1]-1)
    if matrix[third_step] == matrix[forth_step] and matrix[third_step] != 0:
        # already filled and the same
        pass #return matrix
    if matrix[third_step] == matrix[forth_step] and matrix[third_step] == 0:
        # both null
        matrix[third_step] = -1
        matrix[forth_step] = -1
        #return matrix
    if matrix[third_step] != matrix[forth_step]:
        if matrix[third_step] != 0 and matrix[forth_step] != 0:
            # somehow they are different
            return False
        if matrix[third_step] != 0:
            # one of them is not null
            matrix[forth_step] = matrix[third_step]
        else:
            matrix[third_step] = matrix[forth_step]
    return matrix

#@profile
def overlay_well(x_matrix, y_matrix):
    if isinstance(x_matrix, bool) or isinstance(y_matrix, bool):
        return False
    join_possible_x_y_z = False
    possible_x_z = set()
    possible_y_z = set()
    for i,row in enumerate(x_matrix):
        for j,x_value in enumerate(row):
            x_value = int(x_value)
            if x_value > 0:
                y_value = int(y_matrix[i,j])
                if y_value > 0 and x_value != y_value:
                    return False
                elif y_value == -1:
                    possible_y_z.add(x_value)
            elif x_value == -1:
                y_value = int(y_matrix[i,j])
                if y_value > 0:
                    possible_x_z.add(y_value)
                elif y_value == -1:
                    join_possible_x_y_z = True
    if join_possible_x_y_z:
        possible_x_y_z = possible_x_z.union(possible_y_z)
        if len(possible_x_y_z) > 1:
            return False
    else:
        if len(possible_x_z) > 1 or len(possible_y_z) > 1:
            return False
    return True

matrices_overlay =  {}

#@profile
def generate_matrix_table(n, triples):
    matrix_table = numpy.zeros(shape=(n**2, n**3, n**3), dtype=int)
    offset = n**2
    for j_big, triple_big in enumerate(triples):
        for i_big, (two_big, op_matrix_big) in enumerate(triple_big.values):
            if isinstance(op_matrix_big, bool):
                # means False
                continue
            for j, triple in enumerate(triples):
                res = 0
                col_offset = offset-1
                for i, (two, op_matrix) in enumerate(triple.values):
#                    overlay = matrices_overlay.get(str(i) + str(j) + str(i_big) + str(j_big))
#                    if overlay is None:
                    overlay = overlay_well(op_matrix_big, op_matrix)
                    matrices_overlay[str(i) + str(j) + str(i_big) + str(j_big)] = overlay
                    matrices_overlay[str(i_big) + str(j_big) + str(i) + str(j)] = overlay
                    bit = 1 if overlay else 0
#                    if bit:
#                        print op_matrix_big, "\n", op_matrix
#                        print "#############################"
                    res |= bit<<col_offset
                    col_offset -= 1
                matrix_table[i_big, j_big, j] = res
    return matrix_table


def zero_depth_cells(matrix_table):
    zero_depth_cells = []
    for i,cell in enumerate(matrix_table[:,0,:]):
        if cell.any():
            zero_depth_cells.append((i,0))
    return  zero_depth_cells

#@profile
def next_depth_cells(cell, path, matrix_table):
    next_depth_cells = []
    next_depth = cell[1] + 1
    # get bit columns of all previous steps in path
    cols = map(lambda cell: matrix_table[cell[0], cell[1], next_depth], path)
    # overlay them
    res_map = reduce(lambda x,y: x & y, cols)
    bits_ar = range(N**2)
    for i, bit_pos in enumerate(bits_ar):
        if res_map & 1<<bits_ar[-i-1]:
            next_depth_cells.append( (bit_pos, next_depth) )
    return next_depth_cells

all_paths = []
path      = []

def overlay_x_on_y(x_op_table, y_op_table):
    for i,row in enumerate(x_op_table):
        for j,x in enumerate(row):
            if x > 0:
                y_op_table[i,j] = x
    return y_op_table

#@profile
def depth_n(n, matrix_table, triples, current_table):
    global all_paths
    global path
    if n >= N**3:
        all_paths.append(copy(path))
        return True
    if n == 0:
        next_cells = zero_depth_cells(matrix_table)
    else:
        cell = path[-1]
        next_cells = next_depth_cells(cell, path, matrix_table)
    for new_cell in next_cells:
        add_table = triples[new_cell[1]].values[new_cell[0]][1]
        if overlay_well(current_table, add_table):
            path.append(new_cell)
            depth_n(n+1, matrix_table, triples, overlay_x_on_y(add_table, copy(current_table)))
            path.pop()

def traverse_table(n, matrix_table, triples):
    depth_n(0, matrix_table, triples, numpy.zeros((n,n), dtype=int))
    return all_paths

#@profile
def main():
    triples = generate_permutations_of_three(N)
    twos = generate_permutations_of_two(N)
    for triple in triples:
        for two in twos:
            op_matrix = generate_op_matrix(triple, two, N)
            triple.values.append( (two,op_matrix) )
    try:
        matrix_table = numpy.load("m_table.dmp.npy")
    except Exception as e:
        matrix_table = generate_matrix_table(N, triples)
        numpy.save("m_table.dmp", matrix_table)
    print "Matrix built"
    all_paths = traverse_table(N, matrix_table, triples)

#    all_op_tables = []
#    for i,path in enumerate(all_paths):
#        table = numpy.zeros( (3,3), dtype=int )
#        for cell in path:
#            op_table = triples[cell[1]].values[cell[0]][1]
#            for i,row in enumerate(op_table):
#                for j,cell in enumerate(row):
#                    if cell > 0:
#                        table[i,j] = cell-1
#        all_op_tables.append(table)
#
#    good_tables = get_good_tables()
#
#    for i,t in enumerate(all_op_tables):
#        print t
#        try:
#            print good_tables[i]
#        except Exception:
#            print "Fuck"
#        print "################"

    print all_paths
    print len(all_paths)
#    print all_op_tables

if __name__ == "__main__":
    main()
