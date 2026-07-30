"""Сущность пользователя.

Содержит класс User для управления данными пользователя:
- Хранит данные аутентификации и профиля
- Предоставляет методы для CRUD-операций через userlib2

Attributes:
    id: Уникальный идентификатор пользователя
    user_name: Логин
    password: Хешированный пароль
    firstname: Имя
    lastname: Фамилия
    latitude: Широта (для расчёта расстояний)
    longitude: Долгота (для расчёта расстояний)
"""


from config import DEFAULT_USER


class User:
    """Класс пользователя приложения.

    Example:
        >>> user = User(1, {'user_name': 'test', 'password': 'hash', ...})
        >>> user.add_to_db()        # сохранить в БД
        >>> user = User.from_db(1)  # загрузить из БД
    """

    def __init__(self, id = '', user=DEFAULT_USER):
        """Инициализирует пользователя.

        Args:
            id: Уникальный идентификатор
            user (dict): Словарь с данными пользователя.
                По умолчанию DEFAULT_USER из config.py
        """
        self.id = id
        self.username = user['username']
        self.password = user['password']
        self.firstname = user['firstname']
        self.lastname = user['lastname']
        self.latitude = user['latitude']
        self.longitude = user['longitude']

    def __str__(self):
        """Возвращает строковое представление (id + имя + фамилия)."""
        return str(self.id) + ' ' + self.firstname + ' ' + self.lastname

    def add_to_db(self):
        """Сохраняет пользователя в таблицу USERS."""
        from DAL import userlib2
        userlib2.create_user(self)

    @staticmethod
    def from_db(user_id = None, username = None):
        from DAL import userlib2
        if user_id is not None:
            return User(user = userlib2.get_user(user_id))
        if username is not None:
            return User(user = userlib2.get_user(username, mode='username'))
        else:
            return None

    def update_db(self):
        from DAL import userlib2
        """Обновляет данные пользователя в таблице USERS."""
        userlib2.update_user(self)

    def delete_db(self):
        from DAL import userlib2
        """Удаляет пользователя из таблицы USERS."""
        userlib2.delete_user(self)
