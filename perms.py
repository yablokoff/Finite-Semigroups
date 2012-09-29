__author__ = 'yablokoff'

from  copy import copy
import numpy
from scipy.sparse import lil_matrix

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
    empty_matrix = numpy.zeros((n,n), dtype=int)
    if not set_value(triple.triple[0], triple.triple[1], two[0], matrix):
        return empty_matrix
    if not set_value(triple.triple[1], triple.triple[2], two[1], matrix):
        return empty_matrix
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
            return empty_matrix
        if matrix[third_step] != 0:
            # one of them is not null
            matrix[forth_step] = matrix[third_step]
        else:
            matrix[third_step] = matrix[forth_step]
    return matrix

@profile
def overlay_well(x_matrix, y_matrix):
    def overlay_of_z(z_inds_set, matrix):
        non_zero_value = 0
        for z_index in z_inds_set:
            if matrix[z_index] > 0:
                if non_zero_value == 0:
                    non_zero_value = matrix[z_index]
                elif matrix[z_index] != non_zero_value:
                    return False
                else:
                    continue
        return True

    if not x_matrix.any() or not y_matrix.any():
        return False
    x_inds = zip(list(x_matrix.nonzero()[0]), list(x_matrix.nonzero()[1]))
    y_inds = zip(list(y_matrix.nonzero()[0]), list(y_matrix.nonzero()[1]))
    for index in x_inds:
        if x_matrix[index] < 0:
            continue
        if x_matrix[index] != y_matrix[index] and y_matrix[index] > 0:
            return False
    for index in y_inds:
        if y_matrix[index] < 0:
            continue
        if y_matrix[index] != x_matrix[index] and x_matrix[index] > 0:
            return False

    x_z_inds = filter(lambda cell: x_matrix[cell] < 0, x_inds)
    if len(x_z_inds) == 1:
        x_z_inds = []
    y_z_inds = filter(lambda cell: y_matrix[cell] < 0, y_inds)
    if len(y_z_inds) == 1:
        y_z_inds = []
    if set(x_z_inds).intersection(y_z_inds):
        z_inds_set = set(x_z_inds + y_z_inds)
        if not overlay_of_z(z_inds_set, x_matrix):
            return False
        if not overlay_of_z(z_inds_set, x_matrix):
            return False
    else:
        if not overlay_of_z(set(x_z_inds), y_matrix):
            return False
        if not overlay_of_z(set(y_z_inds), x_matrix):
            return False
    return True

@profile
def generate_matrix_table(n, triples):
    matrix_table = numpy.zeros(shape=(n**2, n**3, n**3), dtype=int)
    offset = n**2
    for j_big, triple_big in enumerate(triples):
        for i_big, (two_big, op_matrix_big) in enumerate(triple_big.values):
            if not op_matrix_big.any():
                continue
            for j, triple in enumerate(triples):
                res = 0
                col_offset = offset-1
                for i, (two, op_matrix) in enumerate(triple.values):
                    bit = 1 if overlay_well(op_matrix_big, op_matrix) else 0
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
path     = []

def depth_n(n, matrix_table):
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
        path.append(new_cell)
        depth_n(n+1, matrix_table)
        path.pop()

def traverse_table(matrix_table):
    depth_n(0, matrix_table)
    return all_paths


def main():
    triples = generate_permutations_of_three(N)
    twos = generate_permutations_of_two(N)
    for triple in triples:
        for two in twos:
            op_matrix = generate_op_matrix(triple, two, N)
            triple.values.append( (two,op_matrix) )
    matrix_table = generate_matrix_table(N, triples)
    all_paths = traverse_table(matrix_table)
    print all_paths
    print len(all_paths)

if __name__ == "__main__":
    main()