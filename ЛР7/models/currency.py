class Currency:
    def __init__(self, i_d, num_code, char_code, name, value, nominal):
        self.i_d = i_d
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal

    # Геттеры
    @property
    def i_d(self):
        return self._i_d

    @property
    def num_code(self):
        return self._num_code

    @property
    def char_code(self):
        return self._char_code

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def nominal(self):
        return self._nominal



    # Сеттеры
    @i_d.setter
    def i_d(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("ID must be positive integer or 0")
        self._i_d = value

    @num_code.setter
    def num_code(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("number code must be positive integer or 0")
        self._num_code = value

    @char_code.setter
    def char_code(self, value):
        if not isinstance(value, str):
            raise ValueError("char code must be string")
        self._char_code = value

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("value must be string")
        self._name = value

    @value.setter
    def value(self, input_value):
        if not isinstance(input_value, float) or input_value < 0:
            raise ValueError("value must be positive float or 0")
        self._value = input_value

    @nominal.setter
    def nominal(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("value must be positive integer")
        self._nominal = value




