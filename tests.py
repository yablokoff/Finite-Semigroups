__author__ = 'yablokoff'

import unittest
from scipy.sparse import lil_matrix

from perms import overlay_well

class TestMatricesSimpleOverlay(unittest.TestCase):

    def setUp(self):
        self.x = lil_matrix((3,3), dtype=int)
        self.x[0,0] = 1
        self.x[2,1] = -1
        self.x[2,2] = -1
        self.y = lil_matrix((3,3), dtype=int)
        self.y[0,0] = 1
        self.y[2,1] = 2
        self.y[2,2] = -1

    def testOverlay(self):
        res = overlay_well(self.x, self.y)
        self.assertTrue(res)

class TestMatricesSimpleOverlay2(unittest.TestCase):

    def setUp(self):
        self.x = lil_matrix((3,3), dtype=int)
        self.x[0,0] = 1
        self.x[2,1] = -1
        self.x[2,2] = -1
        self.y = lil_matrix((3,3), dtype=int)
        self.y[0,0] = 1
        self.y[1,2] = -1
        self.y[2,1] = 2
        self.y[2,2] = -1

    def testOverlay(self):
        res = overlay_well(self.x, self.y)
        self.assertTrue(res)

class TestMatricesSimpleOverlay3(unittest.TestCase):

    def setUp(self):
        self.x = lil_matrix((3,3), dtype=int)
        self.x[0,0] = 1
        self.x[2,0] = -1
        self.x[2,0] = -1
        self.y = lil_matrix((3,3), dtype=int)
        self.y[0,0] = -1
        self.y[1,0] = 2
        self.y[2,0] = -1
        self.y[1,1] = 1

    def testOverlay(self):
        res = overlay_well(self.x, self.y)
        self.assertTrue(res)

class TestMatricesSimpleOverlay4(unittest.TestCase):

    def setUp(self):
        self.x = lil_matrix((3,3), dtype=int)
        self.x[0,0] = 1
        self.x[1,0] = 1
        self.x[2,0] = -1
        self.x[2,0] = -1
        self.y = lil_matrix((3,3), dtype=int)
        self.y[0,0] = -1
        self.y[1,0] = 2
        self.y[2,0] = -1

    def testOverlay(self):
        res = overlay_well(self.x, self.y)
        self.assertFalse(res)

if __name__ == "__main__":
    unittest.main()

