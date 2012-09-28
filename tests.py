__author__ = 'yablokoff'

import unittest
from scipy.sparse import lil_matrix

from perms import overlay_matrices

class TestMatricesSimpleOverlay(unittest.TestCase):

    def setUp(self):
        self.x = lil_matrix((3,3), dtype=int)
        self.x[1,1] = 2
        self.y = lil_matrix((3,3), dtype=int)
        self.y[0,0] = 1
        self.y[1,1] = -1
        self.y[1,2] = -1
        self.x_free_cells = []
        self.y_free_cells = [set([(1,1), (1,2)])]

    def testOverlay(self):
        res_matrix, res_free_cells = overlay_matrices(self.x, self.x_free_cells, self.y, self.y_free_cells)
        desired_res = lil_matrix((3,3), dtype=int)
        desired_res[0,0] = 1
        desired_res[1,1] = 2
        desired_res[1,2] = 2
        self.assertTrue( (res_matrix.todense() == desired_res.todense()).all() )
        self.assertEqual(res_free_cells, [])

class TestMatricesOverlayWith2FreeCells(unittest.TestCase):

    def setUp(self):
        self.x = lil_matrix((3,3), dtype=int)
        self.x[0,0] = -1
        self.x[1,1] = 2
        self.y = lil_matrix((3,3), dtype=int)
        self.y[0,0] = 1
        self.y[1,1] = -1
        self.y[1,2] = -1
        self.x_free_cells = [set([(0,0)])]
        self.y_free_cells = [set([(1,1), (1,2)])]

    def testOverlay(self):
        res_matrix, res_free_cells = overlay_matrices(self.x, self.x_free_cells, self.y, self.y_free_cells)
        desired_res = lil_matrix((3,3), dtype=int)
        desired_res[0,0] = 1
        desired_res[1,1] = 2
        desired_res[1,2] = 2
        self.assertTrue( (res_matrix.todense() == desired_res.todense()).all() )
        self.assertEqual(res_free_cells, [])


if __name__ == "__main__":
    unittest.main()

