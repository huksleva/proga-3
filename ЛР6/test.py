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
    def test_all_currencies_missing_logs_each_and_returns_none(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"Valute": {}}
        mock_get.return_value = mock_response

        captured_output = StringIO()
        sys.stdout = captured_output

        result = get_currencies(['BTC', 'ETH'])

        sys.stdout = self.held_stdout

        self.assertIsNone(result)
        output = captured_output.getvalue()
        self.assertIn("Валюта 'BTC' отсутствует", output)
        self.assertIn("Валюта 'ETH' отсутствует", output)


if __name__ == '__main__':
    unittest.main()