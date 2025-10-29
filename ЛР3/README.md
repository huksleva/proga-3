# Лабораторная работа №3

## Описание

Данный проект реализует генерацию двоичного дерева с использованием рекурсивного алгоритма и предоставляет инструменты для его тестирования. Дерево представляется в виде **вложенного словаря**, где каждый узел содержит:

- `"value"` — значение узла,
- `"left"` — левое поддерево (или отсутствует, если поддерева нет),
- `"right"` — правое поддерево (или отсутствует, если поддерева нет).

Алгоритм позволяет задавать произвольные функции для вычисления значений левого и правого потомков, что делает реализацию гибкой и пригодной для различных вариантов заданий.

## Структура проекта

- `myCode.py` — основной модуль с функцией генерации дерева
- `test.py` — модуль для автоматизированного тестирования с использованием `unittest`

## Функция

### `gen_bin_tree(height, root=1, left_leaf=None, right_leaf=None)`

**Назначение:**  
Рекурсивно генерирует двоичное дерево заданной высоты и возвращает его в виде вложенного словаря.

**Параметры:**
- `height` (`int`): высота дерева.  
  - При `height == 0` дерево состоит только из корневого узла.  
  - При `height < 0` возвращается пустой словарь `{}`.
- `root` (`Any`, опционально): значение корневого узла (по умолчанию `1`).
- `left_leaf` (`Callable[[Any], Any]` или `None`, опционально): функция для вычисления значения левого потомка из значения родителя. По умолчанию: `lambda x: x * 2`.
- `right_leaf` (`Callable[[Any], Any]` или `None`, опционально): функция для вычисления значения правого потомка. По умолчанию: `lambda x: x + 3`.

**Возвращает:**  
`dict` — вложенный словарь, описывающий структуру дерева. Каждый узел имеет ключ `"value"`, а при наличии потомков — также `"left"` и/или `"right"`.

**Примеры:**

```python
gen_bin_tree(height=0, root=5)
# Результат: {"value": 5}

gen_bin_tree(height=1, root=1)
# Результат:
# {
#   "value": 1,
#   "left": {"value": 2},   # 1 * 2
#   "right": {"value": 4}   # 1 + 3
# }
```

## Тестирование

Файл `test.py` содержит модульные тесты с использованием библиотеки `unittest`.

### Класс `TestGenBinTree`

Методы:
- `test_height_0` — проверяет корректность дерева высоты 0 (только корень).
- `test_height_1_default_funcs` — проверяет дерево высоты 1 с функциями по умолчанию.
- `test_height_2_custom_funcs` — проверяет дерево высоты 2 с пользовательскими функциями.
- `test_negative_height` — проверяет поведение при отрицательной высоте (возвращает `{}`).
- `test_return_type` — убеждается, что функция всегда возвращает объект типа `dict`.

#### Все тесты гарантируют корректность рекурсивной генерации дерева и обработки граничных случаев.

## Запуск тестов

```bash
python -m unittest test.py
```

## Листинг кода
**myCode.py:**
```python
import json
from typing import Any, Callable, Optional


def gen_bin_tree(
    height: int,
    root: Any = 1,
    left_leaf: Optional[Callable[[Any], Any]] = None,
    right_leaf: Optional[Callable[[Any], Any]] = None
) -> dict:
    """Рекурсивно генерирует двоичное дерево в виде вложенного словаря.

     Дерево представлено в виде словаря с ключами "value", "left" и "right".
     - "value" содержит значение узла.
     - 'left' и 'right' содержат левое и правое поддеревья (или ни одно из них, если оно отсутствует).

     Аргументы:
     высота (int): Высота дерева. Должно быть >= 0.
     Высота 0 означает, что дерево состоит только из корневого узла.
     root (любое, необязательно): значение корневого узла. Значение по умолчанию равно 1.
     left_leaf (вызываемое, необязательно): Функция для вычисления значения левого дочернего
    элемента из значения родительского. По умолчанию используется лямбда x: x * 2.
     right_leaf (вызываемая, необязательная): функция для вычисления правильного дочернего значения
    из родительского значения. По умолчанию используется лямбда x: x + 3.

     Возвращается:
     dict: Вложенный словарь, представляющий двоичное дерево.

     База рекурсии:
     - Если height < 0, возвращает пустой словарь {}.
     - Если height == 0, возвращает {'значение': root}.
    """

    # Set default lambda functions if not provided
    if left_leaf is None:
        left_leaf = lambda x: x * 2
    if right_leaf is None:
        right_leaf = lambda x: x + 3

    # Handle invalid height
    if height < 0:
        return {}

    # Base case: height == 0 → leaf node (no children)
    if height == 0:
        return {"value": root}

    # Recursive case: build left and right subtrees
    left_subtree = gen_bin_tree(
        height - 1,
        left_leaf(root),
        left_leaf,
        right_leaf
    )
    right_subtree = gen_bin_tree(
        height - 1,
        right_leaf(root),
        left_leaf,
        right_leaf
    )

    return {
        "value": root,
        "left": left_subtree,
        "right": right_subtree
    }


# Example usage
if __name__ == "__main__":
    tree = gen_bin_tree(height=5, root=1)
    print(json.dumps(tree, indent=2))
```

**test.py**
```python
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
```

## Примечания

- Дерево строится рекурсивно, и каждый узел явно содержит свои поддеревья.
- Функции `left_leaf` и `right_leaf` могут быть заменены на любые вызываемые объекты, принимающие одно значение и возвращающие новое.
- При высоте `0` узел не имеет потомков.
- При отрицательной высоте возвращается пустой словарь.

## Возможные улучшения

- Добавить функцию для визуализации дерева в консоли или в графическом виде.
- Реализовать сериализацию/десериализацию дерева в/из JSON.
- Поддержка несимметричных деревьев (например, когда левое и правое поддеревья имеют разную глубину).



