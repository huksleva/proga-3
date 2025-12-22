# models/app.py

from .author import Author

class App:
    """
    Модель приложения.
    Содержит название, версию и ссылку на автора.
    """

    def __init__(self, name: str = "PROGA3", version: str = "V2.0", author: Author = None):
        self.name = name
        self.version = version
        self.author = author or Author()  # если не передан — создаём дефолтного

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Название приложения не может быть пустым")
        self._name = value.strip()

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Версия приложения должна быть непустой строкой")
        self._version = value.strip()

    @property
    def author(self) -> Author:
        return self._author

    @author.setter
    def author(self, value: Author):
        if not isinstance(value, Author):
            raise TypeError("Автор должен быть объектом класса Author")
        self._author = value