import unittest
from myCode import gen_bin_tree


class TestGenBinTree(unittest.TestCase):

    def test_height_0(self):
        """Тест: дерево высоты 0 — только корень."""
        result = gen_bin_tree(height=0, root=5)
        expected = {"value": 5}
        self.assertEqual(result, expected)

    def test_height_1_default_funcs(self):
        """Тест: дерево высоты 1 с функциями по умолчанию."""
        result = gen_bin_tree(height=1, root=1)
        expected = {
            "value": 1,
            "left": {"value": 2},   # 1 * 2
            "right": {"value": 4}   # 1 + 3
        }
        self.assertEqual(result, expected)

    def test_height_2_custom_funcs(self):
        """Тест: дерево высоты 2 с пользовательскими функциями."""
        left_f = lambda x: x + 10
        right_f = lambda x: x - 1
        result = gen_bin_tree(height=2, root=3, left_leaf=left_f, right_leaf=right_f)
        expected = {
            "value": 3,
            "left": {
                "value": 13,           # 3 + 10
                "left": {"value": 23}, # 13 + 10
                "right": {"value": 12} # 13 - 1
            },
            "right": {
                "value": 2,            # 3 - 1
                "left": {"value": 12}, # 2 + 10
                "right": {"value": 1}  # 2 - 1
            }
        }
        self.assertEqual(result, expected)

    def test_negative_height(self):
        """Тест: отрицательная высота → пустой словарь."""
        result = gen_bin_tree(height=-1, root=1)
        self.assertEqual(result, {})

    def test_return_type(self):
        """Тест: функция всегда возвращает dict."""
        self.assertIsInstance(gen_bin_tree(0, 1), dict)
        self.assertIsInstance(gen_bin_tree(2, 5), dict)
        self.assertIsInstance(gen_bin_tree(-5, 10), dict)


if __name__ == "__main__":
    unittest.main()