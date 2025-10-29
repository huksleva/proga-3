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
