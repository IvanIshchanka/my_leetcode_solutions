"""238. Product of Array Except Self  [Medium]

https://leetcode.com/problems/product-of-array-except-self/

Pattern: prefix-suffix

--- Problem statement ---
Дан массив целых чисел nums. Вернуть массив answer, где answer[i] равен
произведению всех элементов nums, КРОМЕ nums[i].

Делением пользоваться нельзя. Алгоритм должен работать за O(n).
Выходной массив не считается дополнительной памятью.

Constraints: 2 <= len(nums) <= 10^5, -30 <= nums[i] <= 30,
произведение любого префикса/суффикса влезает в 32-битный int.

--- Approach ---
  1. Брутфорс: для каждого i перемножать все остальные — O(n^2).
     Через деление было бы O(n), но деление запрещено (и ломается на нулях).
  2. answer[i] = (произведение всего слева от i) * (произведение всего
     справа от i). Оба множителя набираются одной бегущей переменной:
     первый проход слева кладёт в result префиксы, второй справа домножает
     на суффиксы.
  3. Инвариант: в обоих проходах running записывается в result[i] ДО того,
     как в него включат сам nums[i]. Поэтому nums[i] никогда не попадает
     в собственный ответ — это и заменяет запрещённое деление.

Complexity: time O(n), space O(1) сверх выходного массива

--- Trigger ---
TODO (fill in AFTER solving): what in the problem statement should have
made you think "prefix-suffix" within 90 seconds?
"""


def product_except_self(nums: list[int]) -> list[int]:
    l = len(nums)
    result = []
    running = 1
    for i in range(l):
        result.append(running)
        running *= nums[i]
    running = 1
    for i in range(l - 1, -1, -1):
        result[i] *= running
        running *= nums[i]
    return result


# TODO с ревью (повтор 2026-08-26 — второй проход воспроизведён без опоры
# на подсказку, но чистка имён не сделана):
#   - l всё ещё здесь и всё ещё путается с единицей (линтеры: E741).
#     Оба цикла обходятся без неё:
#       for num in nums                      — первый проход
#       for i in reversed(range(len(nums)))  — второй
#   - running под две разные роли: prefix в первом проходе, suffix во втором.
#     Из имени должно быть видно, какая половина сейчас набирается
#   - уметь объяснить, почему решение не ломается на нулях (там, где
#     подход «перемножить всё и поделить» разваливается)


def test_example_1():
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]


def test_edge_case():
    """Нули — тот случай, на котором разваливается трюк с делением."""
    assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]


def test_two_zeros_make_everything_zero():
    assert product_except_self([0, 4, 0]) == [0, 0, 0]


def test_negatives():
    assert product_except_self([-1, -2, -3, -4]) == [-24, -12, -8, -6]


def test_minimum_length():
    """len(nums) == 2: каждый элемент — это просто сосед."""
    assert product_except_self([2, 3]) == [3, 2]
