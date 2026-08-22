"""242. Valid Anagram  [Easy]

https://leetcode.com/problems/valid-anagram/

Pattern: counting

--- Problem statement ---
Даны строки s и t. Вернуть True, если t — анаграмма s, то есть t состоит
ровно из тех же символов с теми же кратностями, в другом порядке.

Constraints: 1 <= len(s), len(t) <= 5 * 10^4, только строчные латинские буквы.

--- Approach ---
  1. Брутфорс: отсортировать обе строки и сравнить — O(n log n).
  2. Считать частоты символов в каждой строке и сравнить два счётчика:
     порядок не важен, важны только кратности.
  3. Инвариант: если каждая буква s встречается в t столько же раз И длины
     совпадают, то у t не может остаться «лишних» букв, которых нет в s.

Complexity: time O(n + m), space O(k) — k различных символов; для a-z это O(1)

--- Trigger ---
когда нужно понять что счетчики значений среди двух массивов совпадают ->
наталкивает на мапу или сет
"""


def is_anagram(s: str, t: str) -> bool:
    def counter(string):
        result = dict()
        for letter in string:
            if letter in result:
                result[letter] += 1
            else:
                result[letter] = 1
        return result

    s_counter = counter(s)
    t_counter = counter(t)
    for letter, count in s_counter.items():
        if not t_counter.get(letter) or t_counter[letter] != count:
            return False
    return len(s) == len(t)


# TODO с ревью:
#   - проверку len(s) != len(t) вынести в начало: она и делает алгоритм
#     корректным, и даёт O(1) отсечку до всей работы
#   - вместо "not get(...) or ... != count" писать get(letter, 0) != count
#     ("not x" смешивает «ключа нет» и «значение 0»)
#   - counter короче: result[letter] = result.get(letter, 0) + 1
#   - знать однострочник: Counter(s) == Counter(t)


def test_example_1():
    assert is_anagram("anagram", "nagaram") is True


def test_not_an_anagram():
    assert is_anagram("rat", "car") is False


def test_edge_case():
    """Разная длина при совпадающем наборе букв — тот случай, где падает
    решение без финальной проверки len(s) == len(t)."""
    assert is_anagram("ab", "aab") is False
    assert is_anagram("aab", "ab") is False


def test_same_letters_different_counts():
    assert is_anagram("aacc", "ccac") is False
