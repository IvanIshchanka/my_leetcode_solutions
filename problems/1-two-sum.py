"""1. Two Sum  [Easy]

https://leetcode.com/problems/two-sum/

Pattern: hash-map

--- Problem statement ---
Дан массив целых чисел nums и целое target. Вернуть индексы двух чисел,
дающих в сумме target.

Ровно одно решение существует; один и тот же элемент дважды использовать
нельзя. Порядок индексов в ответе не важен.

Constraints: 2 <= len(nums) <= 10^4, -10^9 <= nums[i], target <= 10^9.

--- Approach ---
  1. Брутфорс: два вложенных цикла по всем парам — O(n^2).
  2. Один проход: для каждого числа искать не пару, а его дополнение
     target - number среди уже увиденных чисел.
  3. Инвариант: в словаре лежат только элементы слева от текущего i,
     поэтому найденная пара всегда состоит из двух разных индексов.

Complexity: time O(n), space O(n)

--- Trigger ---
найти элементы дающие в сумме х -> наталкивает на мапу или сет
"""


def two_sum(nums: list[int], target: int) -> list[int]:
    existing_numbers_dict = dict()
    for i, number in enumerate(nums):
        substraction = target - number
        if substraction in existing_numbers_dict:
            return [existing_numbers_dict[substraction], i]
        else:
            existing_numbers_dict[number] = i


# TODO с ревью:
#   - переименовать substraction -> complement (и опечатка, и смысл)
#   - else лишний: после return управление до него не доходит
#   - добавить явный return [] в конце вместо неявного None
#   - уметь объяснить, почему перезапись индекса при дубликате безопасна


def test_example_1():
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]


def test_pair_not_adjacent():
    assert two_sum([3, 2, 4], 6) == [1, 2]


def test_edge_case():
    """Дубликаты: оба слагаемых — одно и то же значение."""
    assert two_sum([3, 3], 6) == [0, 1]


def test_negatives():
    assert two_sum([-3, 4, 3, 90], 0) == [0, 2]
