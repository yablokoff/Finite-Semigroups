__author__ = 'yablokoff'

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
        return matrix
    if matrix[third_step] == matrix[forth_step] and matrix[third_step] == 0:
        matrix[third_step] = -1
        matrix[forth_step] = -1
        return matrix
    if matrix[third_step] != matrix[forth_step]:
        if matrix[third_step] != 0:
            matrix[forth_step] = matrix[third_step]
        else:
            matrix[third_step] = matrix[forth_step]
        return matrix

def overlay_matrices(matrixx, matrixy):
    x_inds = zip(list(matrixx.nonzero()[0]), list(matrixx.nonzero()[1]))
    x_z_inds = filter(lambda x: x_inds[x[0], x[1]] == -1, x_inds)
    y_inds = zip(list(matrixy.nonzero()[0]), list(matrixy.nonzero()[1]))
    y_z_inds = filter(lambda y: y_inds[y[0], y[1]] == -1, y_inds)


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