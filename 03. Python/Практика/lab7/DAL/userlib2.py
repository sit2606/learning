"""
userlib2 — библиотека для управления пользователями в SQLite (версия 2).

Модуль предоставляет CRUD-функции для работы с пользователями
через таблицу USERS в SQLite.

Функции:
- create_user(user): добавляет пользователя (User) в таблицу USERS
- get_user(pattern, mode): читает пользователя по username или id (возвращает dict)
- update_user(user): обновляет данные пользователя (User)
- delete_user(user): удаляет пользователя (User) по id

Использование:
    from DAL.userlib2 import create_user, get_user, update_user
"""

import sqlite3

from models.entities.user import User

field_names = ['Id',
               'user_name',
               'password',
               'firstname',
               'lastname',
               'latitude',
               'longitude']

from config import DATABASE_PATH, DEFAULT_USER

def create_user(user: User  = User(DEFAULT_USER)):

    """Добавляет пользователя в таблицу USERS.

    Args:
        user (User): Объект пользователя. По умолчанию User(DEFAULT_USER).
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT OR IGNORE INTO USERS ( username, password, firstname, lastname, latitude, longitude) VALUES (?,?,?,?,?,?)",
        (user.username, user.password, user.firstname,
         user.lastname, user.latitude, user.longitude),
    )
    conn.commit()
    conn.close()

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
                res = cursor.fetchone()
                if res is not None:
                    user = dict(res)
                    return user
                else:
                    return DEFAULT_USER
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

def update_user(user: User = User(DEFAULT_USER)):
    """Обновляет данные пользователя в таблице USERS.

    Args:
        user (User): Объект пользователя с обновлёнными данными.
    """
    _user = user
    try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE USERS SET username = ?, password = ?, firstname = ?, lastname = ?, latitude =? , longitude =?    WHERE id = ?",
                (_user.username, _user.password, _user.firstname, _user.lastname, _user.latitude, _user.longitude, _user.id)
            )
            conn.commit()
            conn.close()
    except Exception as e:
        print(e)
        print("Error in update_user")

def delete_user(user: User):
    """Удаляет пользователя из таблицы USERS по id.

    Args:
        user (User): Объект пользователя для удаления.
    """
    try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM  USERS   WHERE id = ?",
                (user.id, )
            )
            conn.commit()
            conn.close()
    except Exception as e:
        print(e)
        print("Error in delete_user")
