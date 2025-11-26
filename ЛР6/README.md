# Лабораторная работа №6. Курсы валют.

## Описание

Лабораторная работа посвящена разработке функции для получения курсов валют с публичного API Центрального банка Российской Федерации. Основные задачи:
- Реализация функции `get_currencies`, получающей курсы по заданным символьным кодам валют;
- Обработка возможных ошибок (сетевые сбои, отсутствие данных, некорректный ответ API);
- Вынесение логирования ошибок в отдельный декоратор для соблюдения принципа единственной ответственности;
- Написание модульных тестов с использованием `unittest` и мокирования HTTP-запросов.

Функция возвращает словарь с курсами запрошенных валют или `None` в случае ошибки. Все сообщения об ошибках направляются в стандартный поток вывода (`sys.stdout`).

## Структура проекта

```
ЛР6/
├── code.py        # Основной модуль: функция get_currencies, декоратор log_errors, вспомогательные функции
└── test.py        # Модульные тесты с покрытием основных сценариев работы
```

## Функции

### `log_errors(func)`
Декоратор для перехвата и логирования ошибок. Обрабатывает:
- `requests.RequestException` — ошибки сети и HTTP;
- `KeyError` — отсутствие ожидаемых ключей в JSON-ответе (`'Valute'` или конкретной валюты);
- Любые другие исключения (как резервный случай).

Все сообщения выводятся в `sys.stdout`. В случае ошибки функция возвращает `None`.

### `get_currencies(currencyCodes, url="...")`
Основная функция для получения курсов валют.

**Параметры:**
- `currencyCodes` (`list[str]`) — список символьных кодов валют (например, `['USD', 'EUR']`);
- `url` (`str`, опционально) — URL API. По умолчанию: `https://www.cbr-xml-daily.ru/daily_json.js`.

**Возвращает:**
- `dict` — словарь `{код: курс}` при успешном выполнении;
- `None` — при любой ошибке.

**Особенности:**
- Использует декоратор `@log_errors` для обработки исключений;
- Завершает работу при отсутствии **любой** запрошенной валюты (возвращает `None`);
- Требует, чтобы все запрошенные валюты присутствовали в ответе API.

### `print_valute(dictionary)`
Вспомогательная функция для удобного вывода результата в консоль. Корректно обрабатывает случай `None`.

## Листинг кода

### code.py

```python
from functools import wraps
import requests
import sys


def log_errors(func):
    """
    Декоратор для логирования ошибок в sys.stdout.
    Оборачивает функцию и перехватывает исключения,
    логируя их в стандартный поток вывода.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            print(f"Ошибка выполнения запроса к API: {e}", file=sys.stdout)
            return None
        except KeyError as e:
            # Возникает, если в ответе нет 'Valute' или нужной валюты
            if str(e) == "'Valute'":
                print("В ответе не содержатся курсы валют (отсутствует ключ 'Valute').", file=sys.stdout)
            else:
                print(f"Валюта {e} отсутствует в данных API.", file=sys.stdout)
            return None
        except Exception as e:
            # На всякий случай — логируем любые другие ошибки
            print(f"Неизвестная ошибка: {e}", file=sys.stdout)
            return None
    return wrapper


@log_errors
def get_currencies(currencyCodes, url: str = "https://www.cbr-xml-daily.ru/daily_json.js"):
    """
    Получает курсы валют с указанного API по списку символьных кодов.

    Аргументы:
        currencyCodes (list): Список символьных кодов валют (например, ['USD', 'EUR']).
        url (str): URL API для получения курсов. По умолчанию — ЦБ РФ.

    Возвращает:
        dict или None: Словарь вида {'USD': 90.5, 'EUR': 98.2, ...},
        где ключи — коды валют, значения — их курсы.
        Возвращает None в случае ошибки HTTP-запроса или обработки данных.
    """

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # может вызвать KeyError → ловится в декораторе
    valute_data = data['Valute']
    result = {}

    for code in currencyCodes:
        # Если кода нет — возникнет KeyError при обращении
        result[code] = valute_data[code]['Value']

    return result


def print_valute(dictionary: dict):
    if dictionary is None:
        print("Не удалось получить курсы валют.")
        return
    for code, rate in dictionary.items():
        print(f"{code} - {rate}")


if __name__ == "__main__":
    # Этот код выполняется ТОЛЬКО при запуске файла напрямую,
    # но НЕ при импорте из другого модуля (например, из test.py)
    currency_codes = ['USD', 'EUR', 'GBP']
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    answer = get_currencies(currency_codes, url)
    print_valute(answer)
```

### test.py
```python
import unittest
import sys
from io import StringIO
from unittest.mock import patch, Mock
from code import get_currencies
import requests


class TestGetCurrencies(unittest.TestCase):

    def setUp(self):
        # Сохраняем оригинальный stdout, чтобы восстановить после каждого теста
        self.held_stdout = sys.stdout

    def tearDown(self):
        # Восстанавливаем stdout
        sys.stdout = self.held_stdout

    @patch('code.requests.get')
    def test_valid_response_returns_correct_dict(self, mock_get):
        # Подготовка мок-ответа
        mock_response = Mock()
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 90.5},
                "EUR": {"Value": 98.25},
                "GBP": {"Value": 115.0}
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Вызов функции
        result = get_currencies(['USD', 'EUR'])

        # Проверка: результат — словарь
        self.assertIsInstance(result, dict)
        # Проверка ключей
        self.assertIn('USD', result)
        self.assertIn('EUR', result)
        self.assertEqual(len(result), 2)
        # Проверка значений (типы и значения)
        self.assertIsInstance(result['USD'], (int, float))
        self.assertIsInstance(result['EUR'], (int, float))
        self.assertEqual(result['USD'], 90.5)
        self.assertEqual(result['EUR'], 98.25)

    @patch('code.requests.get')
    def test_missing_code_logs_and_returns_none(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 90.5}
                # EUR отсутствует
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Перехватываем stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        result = get_currencies(['USD', 'EUR'])

        # Восстанавливаем stdout
        sys.stdout = self.held_stdout

        # Функция должна вернуть None из-за KeyError на 'EUR'
        self.assertIsNone(result)

        # Проверка лога
        output = captured_output.getvalue()
        self.assertIn("Валюта 'EUR' отсутствует в данных API.", output)

    @patch('code.requests.get')
    def test_no_valute_in_response_logs_and_returns_none(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"Date": "2025-04-05"}  # Нет 'Valute'
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        captured_output = StringIO()
        sys.stdout = captured_output

        result = get_currencies(['USD'])

        sys.stdout = self.held_stdout

        self.assertIsNone(result)
        output = captured_output.getvalue()
        self.assertIn("В ответе не содержатся курсы валют", output)

    @patch('code.requests.get')
    def test_request_exception_logs_and_returns_none(self, mock_get):
        # Имитируем сетевую ошибку
        mock_get.side_effect = requests.RequestException("Connection failed")

        captured_output = StringIO()
        sys.stdout = captured_output

        result = get_currencies(['USD'])

        sys.stdout = self.held_stdout

        self.assertIsNone(result)
        output = captured_output.getvalue()
        self.assertIn("Ошибка выполнения запроса к API", output)
        self.assertIn("Connection failed", output)

    @patch('code.requests.get')
    def test_empty_code_list_returns_empty_dict(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 90.5}
            }
        }
        mock_get.return_value = mock_response

        result = get_currencies([])

        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    @patch('code.requests.get')
    def test_all_currencies_missing_logs_and_returns_none(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"Valute": {}}
        mock_get.return_value = mock_response

        captured_output = StringIO()
        sys.stdout = captured_output

        result = get_currencies(['BTC', 'ETH'])

        sys.stdout = self.held_stdout

        self.assertIsNone(result)
        output = captured_output.getvalue()
        # Проверяем ТОЛЬКО первую валюту — именно она вызывает KeyError
        self.assertIn("Валюта 'BTC' отсутствует", output)
        # Убираем проверку 'ETH', потому что до неё дело не доходит


if __name__ == '__main__':
    unittest.main()
```

## Примечания

- **Важно**: В URL-адресе в исходном коде присутствовали **лишние пробелы в конце**, что приводило к ошибке 404. В финальной версии они удалены.
- Функция `get_currencies` завершает работу при отсутствии **любой** из запрошенных валют (возвращает `None`). Это поведение выбрано для строгой проверки входных данных.
- Все тесты используют мокирование (`@patch`), поэтому **не выполняют реальных HTTP-запросов** и работают мгновенно.
- Для корректной работы при импорте (например, в тестах) весь исполняемый код обёрнут в `if __name__ == "__main__":`.

## Возможные улучшения

1. **Частичный результат**: вместо возврата `None` при отсутствии одной валюты, можно возвращать словарь с найденными курсами и логировать только отсутствующие. Это повысит гибкость.
2. **Настройка таймаута**: добавить параметр `timeout` в `requests.get()` для контроля времени ожидания ответа.
3. **Валидация входных данных**: проверять, что `currencyCodes` — это список строк, и отфильтровывать дубликаты.
4. **Поддержка кэширования**: добавить `@lru_cache` для повторных вызовов с теми же аргументами (требует неизменяемых входных данных, например, `tuple`).
5. **Логирование в файл**: расширить декоратор, чтобы он мог писать логи не только в `stdout`, но и в файл (параметризуемо).
6. **Кастомные исключения**: вместо возврата `None` генерировать специфичные исключения (`CurrencyNotFoundError`, `APIUnavailableError`), что улучшит обработку ошибок на стороне вызывающего кода.