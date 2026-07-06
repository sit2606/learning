"""
App — точка входа приложения для управления фермерскими рынками.

Выполняет:
1. Создание директории files/
2. Инициализацию справочников и парсинг Export.csv
3. Тестирование CRUD пользователей
4. Цикл обработки пользовательских команд (с отслеживанием сессии user)

Использование:
    python App.py
"""
import csv

from BusinessLogic.marketList import get_all_markets_ordered_by_column, get_market_by_id
from DAL import userLib
from DAL.fileLib import create_reference_base
from DAL.referenceLib import get_reference_with_name_as_key, get_all_connections_by_market_id, \
    get_reference_with_uid_as_key
from UI.uiLib import print_welcome
from BusinessLogic.workflowLib import *


def testing():
    """
    Тестирование новых функций (временная функция для отладки).

    Вызывает:
    - create_reference_base() — создание итогового справочника
    - get_all_connections_by_market_id() — получение связей рынка
    - get_reference_with_uid_as_key() — чтение справочника по Id
    - get_market_by_id() — получение данных рынка по Id
    """
    from DAL import userLib
    user_1 = userLib.get_user_by_username('asd')
    user_2 = userLib.get_user_by_username()
    print('a')


def user_lib_testing():
    """
    Демонстрация CRUD-операций с пользователями.

    Проверяет, есть ли пользователи в файле. Если нет — создаёт тестовых
    для проверки работы userLib.
    """
    with open(f"files/USER_INFO.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        len = 0
        for row in reader:
            len += 1
        if len > 1:
            pass
        else:
            fileLib.create_user_base()
            test_user_uid = userLib.create_user()
            test_user = userLib.read_user(test_user_uid)
            test_user['firstname'] = 'TestIngs'
            userLib.update_user(test_user)
            test_user_to_delete = userLib.create_user()
            userLib.create_user()
            userLib.delete_user(test_user_to_delete)


def main():
    """
    Основная функция запуска приложения.

    Порядок выполнения:
    1. directory_creation() — создание папки files/
    2. file_creation() — проверка и инициализация CSV-файлов
    3. user_lib_testing() — тестирование CRUD пользователей
    4. Цикл команд: приветствие, чтение и обработка команд
       с отслеживанием текущего пользователя (user = None при старте)
    """
    #testing()
    directory_creation()
    file_creation()
    user_lib_testing()
    run_app = True
    print_welcome()
    user = None
    while run_app:
        command = get_command(user)
        run_app, user = proceed_command(command, user)


if __name__ == "__main__":
    main()
