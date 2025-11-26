from collections import deque
from typing import Callable, Optional

def gen_bin_tree(
    height: int,
    root: int,
    left_func: Optional[Callable[[int], int]] = lambda x: x*2,
    right_func: Optional[Callable[[int], int]] = lambda x: x+3
) -> dict:
    """
    Нерекурсивная функция для построения бинарного дерева заданной высоты.
    Правила генерации потомков:
        left_child = parent * 2
        right_child = parent + 3
    Возвращает дерево в виде вложенного словаря.
    """

    if height < 0:
        return {}
    elif height == 0:
        return {'value': root, 'left': None, 'right': None}
    else:
        tree = {'value': root, 'left': None, 'right': None}
        queue = deque()
        queue.append((tree, 1))  # (узел, глубина)

        while queue:
            node, depth = queue.popleft()

            if depth >= height:
                continue

            left_val = left_func(node['value'])
            right_val = right_func(node['value'])


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

tree_dict = gen_bin_tree(tree_height, root_value)

print("Бинарное дерево (в виде словаря):")
print(tree_dict)
print("\n--- Визуализация по уровням ---")
print_tree_levels(tree_dict)
print("\n--- Графическая визуализация (с ветвями) ---")
print_tree_graphic(tree_dict)