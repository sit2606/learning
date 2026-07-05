"""
userLib — библиотека для управления пользователями.

Модуль предоставляет CRUD-функции для работы с пользователями
через CSV-файл files/USER_INFO.csv.

Функции:
- create_user(): добавляет пользователя, возвращает UUID
- read_user(user_id): читает пользователя по UUID
- get_user_by_username(username): читает пользователя по логину
- update_user(user): обновляет данные пользователя
- delete_user(user_id): удаляет пользователя по UUID

Использование:
    from DAL.userLib import create_user, read_user, get_user_by_username
"""

import csv
import uuid


field_names = ['Id',
               'user_name',
               'password',
               'firstname',
               'lastname',
               'location']
DEFAULT_USER = {'Id': None,
                'user_name': 'test',
                'password': '',
                'firstname': 'test_firstname',
                'lastname': 'test_lastname',
                'location': 'test_location'}
def create_user(user = DEFAULT_USER):
    _user_to_create = user
    file_path = "files/USER_INFO.csv"
    try:
        with open(file_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            uid = uuid.uuid4()
            writer.writerow([uid, user['user_name'],user['password'], user['firstname'], user['lastname'], user['location']])
            return str(uid)
    except Exception as e:
        print(e)
        print("Error in create_user")

def read_user(user_id):
    try:
        with open(f"files/USER_INFO.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Id"] == user_id:
                    return row
    except Exception as e:
        print(e)
        print("Error in read_user")
def get_user_by_username(username=None):
    """
    Читает пользователя по логину (user_name).

    Args:
        username (str): Логин пользователя.

    Returns:
        dict: данные пользователя или None если не найден.
    """
    try:
        with open(f"files/USER_INFO.csv", "r", newline="", encoding="utf-8") as file:
            user_base = csv.DictReader(file)
            for user in user_base:
                if user["user_name"] == username:
                    return user
    except Exception as e:
        print(e)
        print("Error in read_user")
def update_user(user = DEFAULT_USER):
    _user = user
    try:
        with open(f"files/USER_INFO.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            new_file = []
            for row in reader:
                if _user["Id"] == row["Id"]:
                    row.update(_user)
                new_file.append(row)
        with open(f"files/USER_INFO.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=['Id',
                   'user_name',
                   'password',
                   'firstname',
                   'lastname',
                   'location'])
            writer.writeheader()
            writer.writerows(new_file)
    except Exception as e:
        print(e)
        print("Error in update_user")

def delete_user(user_id):
    _user_id = user_id
    try:
        with open(f"files/USER_INFO.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            new_file = []
            for row in reader:
                if _user_id == row["Id"]:
                    continue
                new_file.append(row)
        with open(f"files/USER_INFO.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=['Id',
                   'user_name',
                   'password',
                   'firstname',
                   'lastname',
                   'location'])
            writer.writeheader()
            writer.writerows(new_file)
    except Exception as e:
        print(e)
        print("Error in delete_user")
