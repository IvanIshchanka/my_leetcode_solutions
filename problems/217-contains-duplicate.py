"""217. Contains Duplicate  [Easy]

https://leetcode.com/problems/contains-duplicate/

Pattern: hash-set

--- Problem statement ---
Дан массив целых чисел nums. Вернуть True, если какое-либо значение
встречается в массиве хотя бы дважды, и False, если все элементы различны.

Constraints: 1 <= len(nums) <= 10^5, -10^9 <= nums[i] <= 10^9.

--- Approach ---
  1. Брутфорс: сравнить каждую пару — O(n^2). Сортировка и проверка
     соседей — O(n log n) время, O(1) доп. памяти.
  2. Один проход: помнить уже увиденные значения в множестве и выходить
     на первом же повторе.
  3. Инвариант: seen — ровно множество элементов слева от текущего,
     поэтому num in seen означает «этот же num уже был раньше».

Complexity: time O(n), space O(n)

--- Trigger ---
понять есть ли дубли в массиве -> наталкивает на мапу или сет
"""


def contains_duplicate(nums: list[int]) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True
        else:
            seen.add(num)
    return False


# TODO с ревью:
#   - else снова лишний
#   - знать однострочник: return len(set(nums)) != len(nums)
#     и его минус — нет раннего выхода, всегда строит множество целиком


def test_example_1():
    assert contains_duplicate([1, 2, 3, 1]) is True


def test_all_distinct():
    assert contains_duplicate([1, 2, 3, 4]) is False


def test_edge_case():
    """Один элемент: дублей быть не может."""
    assert contains_duplicate([1]) is False


def test_duplicate_at_the_very_end():
    assert contains_duplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) is True
