import timeit
import matplotlib.pyplot as plt
from functools import lru_cache


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
@lru_cache(maxsize=None)
def fact_recursive_memo(n):
    if n < 0:
        raise ValueError("Факториал не определён для отрицательных чисел")
    elif n in (0, 1):
        return 1
    else:
        return fact_recursive(n-1)



# Для итеративной мемоизация не даёт преимущества, но для чистоты эксперимента:
# можно использовать тот же подход, хотя он избыточен
@lru_cache(maxsize=None)
def fact_iterative_memo(n):
    if n < 0:
        raise ValueError("Факториал не определён для отрицательных чисел")
    result = 1
    for i in range(2, n + 1):
        result *= i
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