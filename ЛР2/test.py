import unittest
from code import TwoSum


def IsMyType(res):
    indicator = True
    indicator *= isinstance(res, list)
    for i in res:
        indicator *= isinstance(i, list)
        for g in i:
            indicator *= isinstance(g, int)
    return indicator


class Test(unittest.TestCase):

    def test1(self):
        nums = [2, 7, 11, 15]
        target = 9
        result = TwoSum(nums, target)
        self.assertEqual(IsMyType(result), True)
        self.assertEqual(result, [[0, 1]])

    def test2(self):
        nums = [3, 2, 4]
        target = 6
        result = TwoSum(nums, target)
        self.assertEqual(IsMyType(result), True)
        self.assertEqual(result, [[1, 2]])

    def test3(self):
        nums = [3, 3]
        target = 6
        result = TwoSum(nums, target)
        self.assertEqual(IsMyType(result), True)
        self.assertEqual(result, [[0, 1]])

    def test4(self):
        nums = [1, 2, 3, 4, 5, 4, 3, 2, 1]
        target = 5
        result = TwoSum(nums, target)
        self.assertEqual(IsMyType(result), True)
        self.assertEqual(result, [[0, 3], [0, 5], [1, 2], [1, 6], [2, 7], [3, 8], [5, 8], [6, 7]])

    def test5(self):
        nums = [1, 2, 1, 2, 1, 2]
        target = 3
        result = TwoSum(nums, target)
        self.assertEqual(IsMyType(result), True)
        self.assertEqual(result, [[0, 1], [0, 3], [0, 5], [1, 2], [1, 4], [2, 3], [2, 5], [3, 4], [4, 5]])

if __name__ == '__main__':
    unittest.main()
