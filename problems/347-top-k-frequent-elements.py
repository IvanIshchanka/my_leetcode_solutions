"""347. Top K Frequent Elements  [Medium]

https://leetcode.com/problems/top-k-frequent-elements/

Pattern: counting

--- Problem statement ---
Дан массив целых чисел nums и целое k. Вернуть k самых часто встречающихся
элементов. Ответ можно вернуть в любом порядке.

Constraints: 1 <= len(nums) <= 10^5, -10^4 <= nums[i] <= 10^4,
k в диапазоне [1, число различных элементов], ответ гарантированно
единственный.

Follow up: сложность должна быть лучше O(n log n).

--- Approach ---
  1. Брутфорс: посчитать частоты и отсортировать счётчик по убыванию —
     O(m log m). Работает, но даёт ПОЛНЫЙ порядок всех элементов, а нужны
     только k верхних: платим за то, чего не просили.
  2. Частота — не произвольное число, а целое от 1 до n. Раз ключ, по
     которому надо упорядочить, это маленькое целое из известного отрезка,
     сортировка не нужна вовсе: ключ сам работает индексом. Список из
     n + 1 корзин, в корзине i лежат все числа с частотой i (их может быть
     несколько), потом идём с конца и набираем, пока не наберём k.
  3. Инвариант: обход с конца выдаёт числа в порядке невозрастания частоты,
     поэтому первые k набранных и есть k самых частых. Длина n + 1, а не n,
     потому что частота может быть равна n (весь массив из одного числа).

Complexity: time O(n), space O(n)

--- Trigger ---
ну тут очевидно что на каунтеры задача, так как частоту нужно считать, но
вот дальше как отсортировать - это уже сложность. Думаю подсказка что
сложость лучше чем n log n, а значит можно за один проход "что-то"
заполнить. В нашем случае это лист где индекс это частота.
"""


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    counter = dict()
    for num in nums:
        if num in counter:
            counter[num] += 1
        else:
            counter[num] = 1

    list_with_frequency_as_index = [list() for n in nums]
    list_with_frequency_as_index.append(list())
    for key, v in counter.items():
        list_with_frequency_as_index[v].append(key)
    result = []
    for i in range(len(list_with_frequency_as_index) - 1, -1, -1):
        for num in list_with_frequency_as_index[i]:
            result.append(num)
            if len(result) == k:
                return result


# TODO с ревью:
#   - list_with_frequency_as_index -> buckets: имя описывает устройство,
#     а не смысл. Та же привычка, что с dict_with_alphabet_tuples_as_keys
#     в 49 — как устроен контейнер, видно строкой ниже
#   - корзины строятся в два приёма (list comprehension по nums, потом
#     отдельный append). Одной строкой: [[] for _ in range(len(nums) + 1)]
#   - if/else в счётчике: counter[num] = counter.get(num, 0) + 1
#   - выход только через return внутри двойного цикла; по ограничениям
#     задачи k всегда набирается, но снаружи функция молча отдаёт None
#   - знать альтернативу через кучу: heapq.nlargest(k, counter, key=counter.get)
#     — O(n log k), тоже лучше O(n log n), но хуже O(n) корзин


def test_example_1():
    assert sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]


def test_example_2():
    assert top_k_frequent([1], 1) == [1]


def test_example_3():
    assert sorted(top_k_frequent([1, 2, 1, 2, 1, 2, 3, 1, 3, 2], 2)) == [1, 2]


def test_edge_case():
    """Весь массив из одного числа: частота равна n, и корзина с индексом n
    обязана существовать — ради этого длина n + 1, а не n."""
    assert top_k_frequent([7, 7, 7], 1) == [7]


def test_k_equals_number_of_unique():
    assert sorted(top_k_frequent([1, 2, 3], 3)) == [1, 2, 3]
