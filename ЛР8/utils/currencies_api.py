# utils/currencies_api.py

import requests
from xml.etree import ElementTree as ET
from models.currency import Currency

def get_currencies():
    """
    Получает список всех валют с официального сайта ЦБ РФ.
    Возвращает список объектов Currency.
    """
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response.encoding = 'windows-1251'  # Кодировка XML от ЦБ
        root = ET.fromstring(response.content)

        currencies = []
        for valute in root.findall('Valute'):
            currencies.append(Currency(
                i_d=valute.get('ID'),  # ← это строка, например "R01235"
                num_code=int(valute.find('NumCode').text),
                char_code=valute.find('CharCode').text,
                name=valute.find('Name').text,
                value=float(valute.find('Value').text.replace(',', '.')),
                nominal=int(valute.find('Nominal').text)
            ))
        return currencies
    except Exception as e:
        print(f"Ошибка загрузки курсов: {e}")
        return []