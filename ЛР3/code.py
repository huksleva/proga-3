def gen_bin_tree(root: int, height: int, i=0, dictionary=None):
    if height == 0:
        return None

    dictionary.update({i: root})


    l = i * 2 + 1
    r = i * 2 + 2

    left_leaf = root * 2
    right_leaf = root + 3

    gen_bin_tree(left_leaf, height - 1, l, dictionary)
    gen_bin_tree(right_leaf, height - 1, r, dictionary)

    return dictionary


def print_heap_tree(tree_dict, index=0, prefix="", is_last=True):
    """
    Красиво выводит бинарное дерево, представленное словарём по индексам кучи.

    tree_dict: dict, где ключи — индексы узлов (0, 1, 2, ...), значения — данные узлов.
    index: текущий индекс (по умолчанию 0 — корень)
    prefix: строка отступов для текущего уровня
    is_last: является ли узел последним у родителя (для правильного рисования ветвей)
    """
    if index not in tree_dict:
        return

    # Определяем символы ветвей
    branch = "└── " if is_last else "├── "
    print(prefix + branch + str(tree_dict[index]))

    # Вычисляем индексы потомков
    left = 2 * index + 1
    right = 2 * index + 2

    # Проверяем, существуют ли потомки
    has_left = left in tree_dict
    has_right = right in tree_dict

    # Новый префикс для потомков
    new_prefix = prefix + ("    " if is_last else "│   ")

    # Рекурсивно выводим потомков
    if has_left or has_right:
        # Левый потомок (всегда первый)
        if has_left:
            print_heap_tree(tree_dict, left, new_prefix, not has_right)
        # Правый потомок
        if has_right:
            print_heap_tree(tree_dict, right, new_prefix, True)


root = 1
height = 5
# print(gen_bin_tree(root, height))
# print_heap_tree(gen_bin_tree(root, height))
