"""49. Group Anagrams  [Medium]

https://leetcode.com/problems/group-anagrams/

Pattern: hash-map

--- Problem statement ---
Дан массив строк strs. Сгруппировать анаграммы: вернуть список групп, в
каждой из которых лежат строки, состоящие из одних и тех же букв с теми же
кратностями. Порядок групп и порядок строк внутри группы не важен.

Constraints: 1 <= len(strs) <= 10^4, 0 <= len(strs[i]) <= 100,
строки состоят только из строчных латинских букв (возможна пустая строка).

--- Approach ---
  1. Брутфорс: для каждой строки сравнивать её со всеми уже найденными
     группами — O(n^2 * k).
  2. Свести каждую строку к канонической форме (одинаковой у всех анаграмм
     и разной у неанаграмм) и сложить в словарь по этому ключу за один проход.
     Здесь канон — вектор из 26 счётчиков букв, как tuple, чтобы он был
     хешируемым.
  3. Инвариант: две строки — анаграммы тогда и только тогда, когда у них
     совпадают счётчики букв, то есть ровно когда совпадает ключ. Значит
     группа = множество строк с одинаковым ключом.

Complexity: time O(n * k), space O(n * k)  (n строк, k — длина строки;
26 на строку — константа)

--- Trigger ---
надо находить анаграммы и ГРУППИРОВАТЬ их.
главная проблема - определить как ключ сделать корректно
"""


def group_anagrams(strs: list[str]) -> list[list[str]]:
    start = ord("a")

    def to_alphabet_tuple(string):
        alphabet_list = [0] * 26
        for letter in string:
            alphabet_list[ord(letter) - start] += 1
        return tuple(alphabet_list)

    dict_with_alphabet_tuples_as_keys = dict()

    for string in strs:
        a_tuple = to_alphabet_tuple(string)
        if a_tuple in dict_with_alphabet_tuples_as_keys:
            dict_with_alphabet_tuples_as_keys[a_tuple].append(string)
        else:
            dict_with_alphabet_tuples_as_keys[a_tuple] = [string]

    return list(dict_with_alphabet_tuples_as_keys.values())


# TODO с ревью (повтор 2026-08-26 — ord("a") вместо 97 и [0] * 26 на месте):
#   - if/else вокруг словаря всё ещё здесь, четвёртый раз подряд:
#     groups.setdefault(key, []).append(string)  или  defaultdict(list)
#   - dict_with_alphabet_tuples_as_keys -> groups: имя описывает устройство,
#     а не смысл; как называется ключ, и так видно строкой выше
#   - знать альтернативный ключ: tuple(sorted(string)) — короче, но
#     O(k log k) на строку вместо O(k)


def _normalize(groups):
    """Порядок групп и строк внутри группы не специфицирован — сравниваем
    как множество множеств."""
    return sorted(sorted(group) for group in groups)


def test_example_1():
    result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert _normalize(result) == _normalize([["bat"], ["nat", "tan"], ["ate", "eat", "tea"]])


def test_edge_case():
    """Пустая строка — валидный вход и своя собственная группа."""
    assert group_anagrams([""]) == [[""]]


def test_single_string():
    assert group_anagrams(["a"]) == [["a"]]


def test_same_letters_different_counts_are_not_anagrams():
    """aab и abb состоят из одних букв, но кратности разные — разные группы."""
    assert _normalize(group_anagrams(["aab", "abb", "aba"])) == _normalize(
        [["aab", "aba"], ["abb"]]
    )


def test_all_strings_in_one_group():
    result = group_anagrams(["abc", "cba", "bac"])
    assert _normalize(result) == [["abc", "bac", "cba"]]
