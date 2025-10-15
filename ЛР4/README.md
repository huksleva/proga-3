# Лабораторная №4

## Задание
Дан массив целых чисел nums и целочисленное значение переменной target , верните индексы двух чисел таким образом, чтобы они в сумме давали target. У каждого входного набора может не быть решений и может быть только одно решение, если есть элементы дающие в сумме target. Вы не можете  использовать один и тот же элемент дважды (и соответственно индекс тоже). Вы можете вернуть ответ в любом порядке нахождения индексов.

## Листинг кода
## code.py
```python
def TwoSum(nums, target):
    res = []
    for i in range(len(nums)-1):
        for g in range(i+1, len(nums)):
            if nums[i] + nums[g] == target:
                res.append([i, g])
    return res
```

* Внешний цикл i проходит от 0 до len(nums) - 2 (в данном случае только i = 0).
* Внутренний цикл g начинается с i + 1, то есть с 1.
* Проверяется условие: nums[0] + nums[1] == 3 + 3 == 6, что равно target.
* Условие выполняется → выводятся индексы 0 и 1.

## test.py
```python
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

```
* Код проверяет, что функция TwoSum(nums, target) корректно находит индексы двух чисел в списке nums, сумма которых равна заданному значению target.


- Конкретно тестируются пять случаев:
  - [2, 7, 11, 15], target=9 → ожидается [[0, 1]]
  - [3, 2, 4], target=6 → ожидается [[1, 2]]
  - [3, 3], target=6 → ожидается [[0, 1]]
  - [1, 2, 3, 4, 5, 4, 3, 2, 1], target=5 → ожидается [[0, 3], [0, 5], [1, 2], [1, 6], [2, 7], [3, 8], [5, 8], [6, 7]]
  - [1, 2, 1, 2, 1, 2], target=3 → ожидается [[0, 1], [0, 3], [0, 5], [1, 2], [1, 4], [2, 3], [2, 5], [3, 4], [4, 5]]

