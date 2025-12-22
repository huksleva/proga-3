class User:
    def __init__(self, username, i_d):
        self.name = username # вызывает сеттер name
        self.i_d = i_d # вызывает сеттер i_d

    # Геттер для name
    @property
    def name(self) -> str:
        return self._name

    # Сеттер для name
    @name.setter
    def name(self, value):
        if not type(value) == str:
            raise TypeError("name must be a string")
        self._name = value

    # Геттер для id
    @property
    def i_d(self) -> int:
        return self._i_d

    # Сеттер для id
    @i_d.setter
    def i_d(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("ID must be positive integer or 0")
        self._i_d = value

