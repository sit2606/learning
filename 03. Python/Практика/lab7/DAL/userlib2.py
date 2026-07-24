"""
userlib2 — библиотека для управления пользователями в SQLite (версия 2).

Модуль предоставляет CRUD-функции для работы с пользователями
через таблицу USERS в SQLite.

Функции:
- create_user(user): добавляет пользователя в таблицу USERS
- read_user(user_id): читает пользователя по id
- get_user(pattern, mode): читает пользователя по username (mode='username') или id (mode='uid')
- update_user(user): обновляет данные пользователя
- delete_user(user_id): удаляет пользователя по id

Использование:
    from DAL.userlib2 import create_user, read_user, get_user
"""

import csv
import uuid
import sqlite3

field_names = ['Id',
               'user_name',
               'password',
               'firstname',
               'lastname',
               'latitude',
               'longitude']
DEFAULT_USER = {
                'user_name': 'test',
                'password': '',
                'firstname': 'test_firstname',
                'lastname': 'test_lastname',
                'latitude': '',
                'longitude': ''}
from config import DATABASE_PATH

def create_user(user = DEFAULT_USER):
    """
    Добавляет пользователя в таблицу USERS.

    Args:
        user (dict): Словарь с данными пользователя (user_name, password,
            firstname, lastname, latitude, longitude).
            По умолчанию используется DEFAULT_USER.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT OR IGNORE INTO USERS ( username, password, firstname, lastname, latitude, longitude) VALUES (?,?,?,?,?,?)",
        (user["user_name"], user["password"], user["firstname"],
         user["lastname"], user["latitude"], user["longitude"]),
    )
    conn.commit()
    conn.close()

def read_user(user_id):
    """
    Читает данные пользователя по id из таблицы USERS.

    Args:
        user_id (int): ID пользователя.

    Returns:
        dict: данные пользователя или None если не найден.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            f"SELECT * FROM USERS WHERE id = ?",
            (user_id, )
        )
        entry = dict(cursor.fetchone())
        conn.close()
        return entry
    except Exception as e:
        print(e)
        print("Error in read_user")
def get_user(pattern=None, mode = 'username'):
    """
    Читает пользователя по username или id.

    Args:
        pattern: Значение для поиска (username или id).
        mode: Режим поиска — 'username' (по логину) или 'uid' (по id).

    Returns:
        dict: данные пользователя или None если не найден.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    match mode:
        case 'username':
            try:
                cursor.execute(
                    f"SELECT * FROM USERS WHERE username = ?",
                    (pattern,)
                )
                user = dict(cursor.fetchone())
                return user
            except Exception as e:
                print(e)
                print("Error in get_user")
        case 'uid':
            try:
                cursor.execute(
                    f"SELECT * FROM USERS WHERE id = ?",
                    (pattern,)
                )
                user = dict(cursor.fetchone())
                return user
            except Exception as e:
                print(e)
                print("Error in get_user")

def update_user(user = DEFAULT_USER):
    """
    Обновляет данные пользователя в таблице USERS.

    Args:
        user (dict): Словарь с обновляемыми данными. Обязательное поле: id.
    """
    _user = user
    try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE USERS SET username = ?, password = ?, firstname = ?, lastname = ?, latitude =? , longitude =?    WHERE id = ?",
                (_user['username'],_user['password'],_user['firstname'],_user['lastname'], _user['latitude'], _user['longitude'], _user['id'])
            )
            conn.commit()
            conn.close()
    except Exception as e:
        print(e)
        print("Error in update_user")

def delete_user(user_id):
    """
    Удаляет пользователя из таблицы USERS по id.

    Args:
        user_id (int): ID пользователя для удаления.
    """
    _user_id = user_id
    try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM  USERS   WHERE id = ?",
                (_user_id, )
            )
            conn.commit()
            conn.close()
    except Exception as e:
        print(e)
        print("Error in delete_user")
