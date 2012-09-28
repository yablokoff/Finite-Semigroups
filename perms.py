__author__ = 'yablokoff'

from  copy import copy
from scipy.sparse import lil_matrix

N = 5

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

    matrix = lil_matrix((n,n), dtype=int)
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
    free_cells = []
    if matrix[third_step] == -1:
        free_cells.append(set([third_step, forth_step]))
    return matrix, free_cells

def overlay_matrices(x_matrix, x_free_cells, y_matrix, y_free_cells):
    # y - "big" matrix
    def mark_cells_with_value(cells_set, value):
        for cell in cells_set:
            new_matrix[cell] = value

    new_matrix = copy(y_matrix)
    x_inds = zip(list(x_matrix.nonzero()[0]), list(x_matrix.nonzero()[1]))
    for x_cell in x_inds:
        if x_matrix[x_cell] < 0 or new_matrix[x_cell] < 0:
            # later
            continue
        if x_matrix[x_cell] == new_matrix[x_cell]:
            # coincide
            continue
        if x_matrix[x_cell] != new_matrix[x_cell]:
            # don't coincide
            return False
        if new_matrix[x_cell] == 0:
            # add rule to operation
            new_matrix[x_cell] = x_matrix[x_cell]
    new_free_cells = copy(y_free_cells)
    for x_free_cells_set in x_free_cells:
        # should be single actually
        for num, y_free_cells_set in enumerate(y_free_cells):
            if y_free_cells_set.intersection(x_free_cells_set):
                new_free_cells[num] = y_free_cells_set.union(x_free_cells_set)
            else:
                new_free_cells.append(x_free_cells_set)
    # here we should do more complicated merging processes
    for num, free_cells_set in enumerate(new_free_cells[:]):
        non_zero_elem = 0
        for free_cell in free_cells_set:
            if x_matrix[free_cell] != 0:
                if not non_zero_elem:
                    non_zero_elem = x_matrix[free_cell]
                elif x_matrix[free_cell] != non_zero_elem:
                    return False
        if non_zero_elem:
            mark_cells_with_value(free_cells_set, non_zero_elem)
        del new_free_cells[num]
    return new_matrix, new_free_cells


def main():
    triples = generate_permutations_of_three(N)
    twos = generate_permutations_of_two(N)
    for triple in triples:
        for two in twos:
            op_matrix = generate_op_matrix(triple, two, N)
            if op_matrix:
                triple.values.append( (two,op_matrix) )
    for t in triples:
        print t.triple, t.values

if __name__ == "__main__":
    main()