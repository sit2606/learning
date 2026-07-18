"""
App — точка входа приложения для управления фермерскими рынками.

Выполняет:
1. Тестирование новых функций (testing)
2. Создание директории files/
3. Инициализацию справочников и парсинг Export.csv
4. Тестирование CRUD пользователей
5. Цикл обработки пользовательских команд (с отслеживанием сессии user)

Использование:
    python App.py
"""
import csv

from BusinessLogic.marketList import get_all_markets, get_market_by_id
from DAL import userLib, referencelib2, filelib2
from DAL.userLib import get_user
from UI.uiLib import print_welcome, request_filter, request_user_updates
from BusinessLogic.workflowLib import *


def testing():
    """Тестирование новых функций SQLite (версия 2).

    Выполняет:
    1. Инициализацию справочных таблиц (prepare_ref)
    2. Тестирование чтения записей из справочников

    Args:
        None

    Returns:
        None
    """
    referencelib2.read_reference_entry('MEDIA', '4')
    filelib2.prepare_ref()

    referencelib2.read_reference_entry('MEDIA', entry_name='Twitter')


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
    1. testing() — тестирование новых функций (заглушка)
    2. directory_creation() — создание папки files/
    3. file_creation() — проверка и инициализация CSV-файлов
    4. user_lib_testing() — тестирование CRUD пользователей
    5. Цикл команд: приветствие, чтение и обработка команд
       с отслеживанием текущего пользователя (user = None при старте)
    """
    testing()
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
