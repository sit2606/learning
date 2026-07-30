"""
Конфигурация приложения.

Содержит настройки, которые могут отличаться между окружениями.

Использование:
    from config import DATABASE_PATH
"""

DATABASE_PATH = 'database/base.db'

DEFAULT_USER = {
                'username': 'test',
                'password': '',
                'firstname': 'test_firstname',
                'lastname': 'test_lastname',
                'latitude': '',
                'longitude': ''}