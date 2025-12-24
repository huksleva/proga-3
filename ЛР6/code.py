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
        currency_codes (list): Список символьных кодов валют (например, ['USD', 'EUR']).
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