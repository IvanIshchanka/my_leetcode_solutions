"""242. Valid Anagram  [Easy]

https://leetcode.com/problems/valid-anagram/

Pattern: counting

--- Problem statement ---
Даны строки s и t. Вернуть True, если t — анаграмма s, то есть t состоит
ровно из тех же символов с теми же кратностями, в другом порядке.

Constraints: 1 <= len(s), len(t) <= 5 * 10^4, только строчные латинские буквы.

--- Approach ---
  1. Брутфорс: отсортировать обе строки и сравнить — O(n log n).
  2. Посчитать частоты символов в каждой строке и сравнить счётчики целиком:
     порядок не важен, важны только кратности.
  3. Инвариант: равенство словарей — это равенство и множеств ключей, и
     значений сразу. Поэтому лишние буквы в t ловятся тем же сравнением,
     что и разные кратности, и отдельная проверка длин не нужна для
     корректности (в первой версии она была обязательной).

Complexity: time O(n + m), space O(k) — k различных символов; для a-z это O(1)

--- Trigger ---
когда нужно понять что счетчики значений среди двух массивов совпадают ->
наталкивает на мапу или сет
"""


def is_anagram(s: str, t: str) -> bool:
    def to_counter(string):
        result = dict()
        for letter in string:
            if letter in result:
                result[letter] += 1
            else:
                result[letter] = 1
        return result

    t_counter = to_counter(t)
    s_counter = to_counter(s)
    return s_counter == t_counter


# TODO с ревью (повтор 2026-08-25 — сравнение словарей целиком вместо
# ручного обхода с финальной проверкой длин, это чище и короче):
#   - if/else в to_counter вернулся: result[letter] = result.get(letter, 0) + 1
#   - можно добавить в начало if len(s) != len(t): return False — для
#     корректности уже не нужно, но это O(1) отсечка до всей работы
#   - знать однострочник: Counter(s) == Counter(t)


def test_example_1():
    assert is_anagram("anagram", "nagaram") is True


def test_not_an_anagram():
    assert is_anagram("rat", "car") is False


def test_edge_case():
    """Один набор букв, но разная длина — лишний ключ или другая кратность
    ловится тем же сравнением словарей."""
    assert is_anagram("ab", "aab") is False
    assert is_anagram("aab", "ab") is False


def test_same_letters_different_counts():
    assert is_anagram("aacc", "ccac") is False


def test_identical_strings():
    assert is_anagram("abc", "abc") is True
