# models/author.py

class Author:
    """
    Модель автора приложения.
    Содержит имя, группу, возраст и пол.
    """

    def __init__(self, name: str = "Леонид", group: str = "ИВТ 2", age: int = 20, sex: str = "М"):
        self.name = name
        self.group = group
        self.age = age
        self.sex = sex

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Имя автора не может быть пустым")
        self._name = value.strip()

    @property
    def group(self) -> str:
        return self._group

    @group.setter
    def group(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Группа должна быть непустой строкой")
        self._group = value.strip()

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int):
        if not isinstance(value, int) or value < 18 or value > 100:
            raise ValueError("Возраст автора должен быть целым числом от 18 до 100")
        self._age = value

    @property
    def sex(self) -> str:
        return self._sex

    @sex.setter
    def sex(self, value: str):
        if not isinstance(value, str) or value not in ("М", "Ж"):
            raise ValueError("Пол должен быть 'М' или 'Ж'")
        self._sex = value