import unittest
from code import sum


class Test(unittest.TestCase):

    def test1(self):
        nums = [2, 7, 11, 15]
        target = 9
        self.assertEqual(sum(nums, target), [0, 1])

    def test2(self):
        nums = [3, 2, 4]
        target = 6
        self.assertEqual(sum(nums, target), [1, 2])

    def test3(self):
        nums = [3, 3]
        target = 6
        self.assertEqual(sum(nums, target), [0, 1])


