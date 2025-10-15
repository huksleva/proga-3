# Лабораторная №4

## Задание
Разработайте программу на языке Python, которая будет строить бинарное дерево (дерево, в каждом узле которого может быть только два потомка). Отображение результата в виде словаря (как базовый вариант решения задания). Далее исследовать другие структуры, в том числе доступные в модуле collections в качестве контейнеров для хранения структуры бинарного дерева. 

Необходимо реализовать нерекурсивный вариант gen_bin_tree

Алгоритм построения дерева должен учитывать параметры, переданные в качестве аргументов функции. Пример: 

```python
def gen_bin_tree(height=<number>, root=<number>):
    pass
```
Если параметры были переданы, то используются они. В противном случае используются параметры, указанные в варианте.

Дерево должно обладать следующими свойствами:

В корне дерева (root) находится число, которое задает пользователь (индивидуально для студента).
Высота дерева (height) задается пользователем (индивидуально для студента).
Левый (left leaf) и правый потомок (right leaf) вычисляется с использованием алгоритмов, индивидуальных для каждого студента в группе и приведен ниже.
Если ваш номер в группе, больше чем последний номер в списке ниже, начинаете отсчет с начала (пример: если вы под №19, то ваш вариант условия №1)

1. Root = 1; height = 5, left_leaf = root*2, right_leaf = root+3
2. Root = 2; height = 6, left_leaf = root*3, right_leaf = root+4
3. Root = 3; height = 4, left_leaf = root+2, right_leaf = root*3
4. Root = 4; height = 4, left_leaf = root*4, right_leaf = root+1
5. Root = 5; height = 6, left_leaf = root^2, right_leaf = root-2
6. Root = 6; height = 5, left_leaf = (root*2)-2, right_leaf = root+4
7. Root = 7; height = 4, left_leaf = root*3, right_leaf = root-4
8. Root = 8; height = 4, left_leaf = root+root/2, right_leaf = root^2
9. Root = 9; height = 6, left_leaf = root*2+1, right_leaf = 2*root-1
10. Root = 10; height = 5, left_leaf = root*3+1, right_leaf = 3*root-1
11. Root = 11; height = 3, left_leaf = root^2, right_leaf = 2+root^2
12. Root = 12; height = 4, left_leaf = root^3, right_leaf = (root*2)-1
13. Root = 13; height = 3, left_leaf = root+1, right_leaf = root-1
14. Root = 14; height = 4, left_leaf = 2-(root-1), right_leaf = root*2
15. Root = 15; height = 6, left_leaf = 2*(root+1), right_leaf = 2*(root-1)
16. Root = 16; height = 3, left_leaf = root/2, right_leaf = root*2
17. Root = 17; height = 4, left_leaf = (root-4)^2, right_leaf = (root+3)*2
18. Root = 18; height = 5, left_leaf = (root-8)*3, right_leaf = (root+8)*2

## Листинг кода
## code.py
```python
def gen_bin_tree(height: int, root: int) -> dict:
    """
    Нерекурсивная функция для построения бинарного дерева заданной высоты.
    Правила генерации потомков:
        left_child = parent * 2
        right_child = parent + 3
    Возвращает дерево в виде вложенного словаря.
    """
    if height <= 0:
        return {}

    tree = {'value': root, 'left': None, 'right': None}
    queue = [(tree, 1)]  # (узел, глубина)

    while queue:
        node, depth = queue.pop(0)

        if depth >= height:
            continue

        left_val = node['value'] * 2
        right_val = node['value'] + 3

        node['left'] = {'value': left_val, 'left': None, 'right': None}
        queue.append((node['left'], depth + 1))

        node['right'] = {'value': right_val, 'left': None, 'right': None}
        queue.append((node['right'], depth + 1))

    return tree


def print_tree_levels(tree: dict) -> None:
    """
    Визуализирует дерево по уровням — каждая строка = один уровень.
    Более читаемо для высоких деревьев.
    """
    if not tree:
        print("Пустое дерево")
        return

    # Список для хранения узлов каждого уровня
    levels = []
    current_level = [tree]

    while current_level:
        next_level = []
        level_values = []

        for node in current_level:
            if node is None:
                level_values.append("N")  # N = None
                next_level.extend([None, None])
            else:
                level_values.append(str(node['value']))
                next_level.append(node['left'])
                next_level.append(node['right'])

        levels.append(level_values)
        # Если следующий уровень пуст — останавливаемся
        if all(n is None for n in next_level):
            break
        current_level = next_level

    # Определяем максимальную ширину для форматирования
    max_width = len(levels[-1]) * 4  # Примерное значение — можно адаптировать

    # Печатаем уровни
    for i, level in enumerate(levels):
        spacing = max_width // (2 ** (i + 1))  # Уменьшаем отступы с увеличением уровня
        line = ""
        for val in level:
            line += f"{val:^{spacing}}"
        print(line.rstrip())


# Альтернатива: печать в "графическом" стиле (как на скриншоте, но аккуратно)
def print_tree_graphic(tree: dict, indent="", prefix=""):
    """
    Графический вывод дерева с ветвями — как на скриншоте, но без "кривизны".
    Использует символы ─ │ └ ├ для визуализации.
    """
    if tree is None:
        return

    # Печатаем текущий узел
    print(f"{indent}{prefix}{tree['value']}")

    # Определяем префиксы для потомков
    if tree['left'] and tree['right']:
        left_prefix = "├─L: "
        right_prefix = "└─R: "
        next_indent = indent + "│   "
    elif tree['left']:
        left_prefix = "└─L: "
        right_prefix = ""  # нет правого
        next_indent = indent + "    "
    elif tree['right']:
        left_prefix = ""  # нет левого
        right_prefix = "└─R: "
        next_indent = indent + "    "
    else:
        return  # лист — ничего не печатаем дальше

    # Рекурсивно печатаем потомков
    if tree['left']:
        print_tree_graphic(tree['left'], next_indent, left_prefix)
    if tree['right']:
        print_tree_graphic(tree['right'], next_indent, right_prefix)


# Пример использования

root_value = 1
tree_height = 5

tree_dict = gen_bin_tree(height=tree_height, root=root_value)

print("Бинарное дерево (в виде словаря):")
print(tree_dict)
print("\n--- Визуализация по уровням ---")
print_tree_levels(tree_dict)
print("\n--- Графическая визуализация (с ветвями) ---")
print_tree_graphic(tree_dict)
```

Этот код реализует нерекурсивное построение бинарного дерева заданной высоты и корневого значения.
Каждый узел имеет двух потомков: левый вычисляется как `значение * 2`, правый — как `значение + 3`.
Дерево представляется в виде вложенных словарей. Для удобства отладки и анализа предусмотрены
два способа визуализации: по уровням (горизонтально) и в виде графической схемы с ветвями (вертикально),
что делает структуру дерева наглядной и легко читаемой.

## test.py
```python
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
```
Этот код представляет собой набор модульных тестов для функции `gen_bin_tree`, написанных с использованием встроенной библиотеки `unittest`. Тесты проверяют корректность работы функции в различных сценариях:  
- соответствие типа возвращаемого значения (всегда `dict`, включая пустой словарь при недопустимой высоте);  
- правильность структуры дерева для высот 1, 2 и 3 с учётом заданных правил генерации потомков (`left = parent * 2`, `right = parent + 3`);  
- корректную обработку граничных случаев — нулевой и отрицательной высоты (ожидается пустой словарь).  

Тесты обеспечивают надёжную проверку логики построения бинарного дерева и помогают выявить ошибки при изменении реализации функции.

