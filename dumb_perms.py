__author__ = 'yablokoff'

import numpy
import copy

def generate_permutations_of_three(n):
    all_triples = []
    for i in range(0, n):
        for j in range(0, n):
            for k in range(0, n):
                all_triples.append((i, j, k))
    return all_triples


def get_good_tables():
    op_table = numpy.zeros((3, 3), dtype=int)
    triples = generate_permutations_of_three(3)
    good_tables = []
    for i0 in range(3):
        for i1 in range(3):
            for i2 in range(3):
                for i3 in range(3):
                    for i4 in range(3):
                        for i5 in range(3):
                            for i6 in range(3):
                                for i7 in range(3):
                                    for i8 in range(3):
                                        op_table[0, 0] = i0
                                        op_table[0, 1] = i1
                                        op_table[0, 2] = i2
                                        op_table[1, 0] = i3
                                        op_table[1, 1] = i4
                                        op_table[1, 2] = i5
                                        op_table[2, 0] = i6
                                        op_table[2, 1] = i7
                                        op_table[2, 2] = i8
                                        bad = False
                                        for triple in triples:
                                            if op_table[op_table[triple[0], triple[1]], triple[2]] != op_table[
                                                                                                      triple[0],
                                                                                                      op_table[
                                                                                                      triple[1], triple[
                                                                                                                 2]]]:
                                                bad = True
                                                break
                                        if not bad:
                                            good_tables.append(copy.copy(op_table))
    return good_tables