# models/user_currency.py

class UserCurrency:
    """
    Связующая сущность между пользователем и валютой (подписка).

    Представляет запись в таблице "user_currency" в реляционной модели.
    """

    def __init__(self, id: int, user_id: int, currency_id: str):
        """
        Инициализирует подписку.

        :param id: Уникальный идентификатор подписки.
        :param user_id: ID пользователя (ссылка на User.id).
        :param currency_id: ID валюты (ссылка на Currency.identification_number).
        """
        self.id = id
        self.user_id = user_id
        self.currency_id = currency_id

    # === id ===
    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID подписки должен быть положительным целым числом")
        self._id = value

    # === user_id ===
    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("user_id должен быть положительным целым числом")
        self._user_id = value

    # === currency_id ===
    @property
    def currency_id(self) -> str:
        return self._currency_id

    @currency_id.setter
    def currency_id(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("currency_id должен быть непустой строкой")
        self._currency_id = value.strip()