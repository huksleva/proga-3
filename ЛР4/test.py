import unittest
from code import gen_bin_tree


class Test(unittest.TestCase):

    def test_return_type(self):
        """Проверка, что функция возвращает словарь или пустой словарь."""
        result = gen_bin_tree(height=3, root=1)
        self.assertIsInstance(result, dict, "Функция должна возвращать объект типа dict")

        # Проверка для height <= 0
        result_empty = gen_bin_tree(height=0, root=5)
        self.assertIsInstance(result_empty, dict, "При height <= 0 должна возвращаться пустой dict")
        self.assertEqual(result_empty, {}, "При height <= 0 должен возвращаться пустой словарь")

    def test_correct_structure_small_tree(self):
        """Проверка корректности структуры дерева для небольшого случая (height=2, root=1)."""
        expected = {
            'value': 1,
            'left': {'value': 2, 'left': None, 'right': None},
            'right': {'value': 4, 'left': None, 'right': None}
        }
        result = gen_bin_tree(height=2, root=1)
        self.assertEqual(result, expected, "Дерево высоты 2 с корнем 1 построено неверно")

    def test_correct_structure_height_1(self):
        """Проверка дерева высоты 1 — только корень."""
        expected = {'value': 10, 'left': None, 'right': None}
        result = gen_bin_tree(height=1, root=10)
        self.assertEqual(result, expected, "Дерево высоты 1 должно содержать только корень")

    def test_correct_structure_height_3(self):
        """Проверка дерева высоты 3 с корнем 1."""
        # Уровень 1: 1
        # Уровень 2: 2 (1*2), 4 (1+3)
        # Уровень 3:
        #   от 2: 4 (2*2), 5 (2+3)
        #   от 4: 8 (4*2), 7 (4+3)
        expected = {
            'value': 1,
            'left': {
                'value': 2,
                'left': {'value': 4, 'left': None, 'right': None},
                'right': {'value': 5, 'left': None, 'right': None}
            },
            'right': {
                'value': 4,
                'left': {'value': 8, 'left': None, 'right': None},
                'right': {'value': 7, 'left': None, 'right': None}
            }
        }
        result = gen_bin_tree(height=3, root=1)
        self.assertEqual(result, expected, "Дерево высоты 3 с корнем 1 построено неверно")

    def test_negative_height(self):
        """Проверка обработки отрицательной высоты."""
        result = gen_bin_tree(height=-5, root=1)
        self.assertEqual(result, {}, "При отрицательной высоте должно возвращаться {}")

    def test_zero_height(self):
        """Проверка высоты 0."""
        result = gen_bin_tree(height=0, root=100)
        self.assertEqual(result, {}, "При height=0 должно возвращаться {}")



if __name__ == '__main__':
    unittest.main()
