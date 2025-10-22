import timeit
import matplotlib.pyplot as plt


# 1. Реализация функций
def fact_recursive(n):
    if n < 0:
        raise ValueError("Факториал не определён для отрицательных чисел")
    if n == 0 or n == 1:
        return 1
    return n * fact_recursive(n - 1)


def fact_iterative(n):
    if n < 0:
        raise ValueError("Факториал не определён для отрицательных чисел")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


# Мемоизация для рекурсивной функции
_fact_memo = {0: 1, 1: 1}


def fact_recursive_memo(n):
    if n < 0:
        raise ValueError("Факториал не определён для отрицательных чисел")
    if n in _fact_memo:
        return _fact_memo[n]
    _fact_memo[n] = n * fact_recursive_memo(n - 1)
    return _fact_memo[n]


# Для итеративной мемоизация не даёт преимущества, но для чистоты эксперимента:
# можно использовать тот же подход, хотя он избыточен
_fact_iter_memo = {0: 1, 1: 1}


def fact_iterative_memo(n):
    if n < 0:
        raise ValueError("Факториал не определён для отрицательных чисел")
    if n in _fact_iter_memo:
        return _fact_iter_memo[n]
    # Начинаем с последнего известного значения
    start = max(_fact_iter_memo.keys())
    result = _fact_iter_memo[start]
    for i in range(start + 1, n + 1):
        result *= i
        _fact_iter_memo[i] = result
    return result


# 2. Подготовка данных
test_numbers = list(range(0, 101, 10))  # 0, 10, 20, ..., 100
number_of_runs = 5  # Количество прогонов для усреднения

# 3. Измерение времени
results = {
    'recursive': [],
    'iterative': [],
    'recursive_memo': [],
    'iterative_memo': []
}

# Сбросим мемо-кэш перед началом тестов для честного сравнения
_fact_memo.clear()
_fact_memo.update({0: 1, 1: 1})
_fact_iter_memo.clear()
_fact_iter_memo.update({0: 1, 1: 1})

for n in test_numbers:
    print(f"Testing n = {n}...")

    # Рекурсивная (без мемоизации)
    time_rec = timeit.timeit(lambda: fact_recursive(n), number=number_of_runs) / number_of_runs
    results['recursive'].append(time_rec)

    # Итеративная (без мемоизации)
    time_iter = timeit.timeit(lambda: fact_iterative(n), number=number_of_runs) / number_of_runs
    results['iterative'].append(time_iter)

    # Рекурсивная с мемоизацией
    time_rec_memo = timeit.timeit(lambda: fact_recursive_memo(n), number=number_of_runs) / number_of_runs
    results['recursive_memo'].append(time_rec_memo)

    # Итеративная с мемоизацией
    time_iter_memo = timeit.timeit(lambda: fact_iterative_memo(n), number=number_of_runs) / number_of_runs
    results['iterative_memo'].append(time_iter_memo)

# 4. Визуализация
plt.figure(figsize=(12, 8))

plt.plot(test_numbers, results['recursive'], 'o-', label='Рекурсивная', linewidth=2)
plt.plot(test_numbers, results['iterative'], 's-', label='Итеративная', linewidth=2)
plt.plot(test_numbers, results['recursive_memo'], '^-', label='Рекурсивная (мемоизация)', linewidth=2)
plt.plot(test_numbers, results['iterative_memo'], 'd-', label='Итеративная (мемоизация)', linewidth=2)

plt.xlabel('Число n')
plt.ylabel('Время выполнения (секунды)')
plt.title('Сравнение времени вычисления факториала')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.yscale('log')  # Логарифмическая шкала по Y для лучшей читаемости
plt.tight_layout()
plt.show()

# 5. Вывод результатов в текстовом виде
print("\n=== Результаты (время в секундах) ===")
print(f"{'n':>3} | {'Рекурсия':>10} | {'Итерация':>10} | {'Рек+Мемо':>10} | {'Итер+Мемо':>10}")
print("-" * 55)
for i, n in enumerate(test_numbers):
    print(f"{n:>3} | {results['recursive'][i]:>10.6f} | {results['iterative'][i]:>10.6f} | "
          f"{results['recursive_memo'][i]:>10.6f} | {results['iterative_memo'][i]:>10.6f}")