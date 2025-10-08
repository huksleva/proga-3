import unittest
from code import gen_bin_tree


class Test(unittest.TestCase):

    def test1(self):
        root = 1
        height = 5
        d = gen_bin_tree(root, height)
        self.assertIsInstance(d, dict)
        self.assertEqual(d, {0: 1, 1: 2, 3: 4, 7: 8, 15: 16, 16: 11, 8: 7, 17: 14, 18: 10, 4: 5, 9: 10, 19: 20, 20: 13, 10: 8, 21: 16, 22: 11, 2: 4, 5: 8, 11: 16, 23: 32, 24: 19, 12: 11, 25: 22, 26: 14, 6: 7, 13: 14, 27: 28, 28: 17, 14: 10, 29: 20, 30: 13})
