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

from BusinessLogic.commandHandler import register_user
from BusinessLogic.market_queries import get_markets_ordered_by_mode, get_all_markets_ordered_by_column, \
    get_market_by_id
from DAL import userLib
from DAL.datalib2 import get_all_markets, get_market, update_market
from DAL.userlib2 import get_user
from UI.uiLib import print_welcome
from BusinessLogic.workflowLib import *
from models.collections.market_collection import MarketCollection
from models.entities.market import Market
from models.entities.review import Review
from models.entities.user import User


def testing():
    """Тестирование новых функций SQLite (версия 2).

    Выполняет:
    1. Инициализацию справочных таблиц (prepare_refs)
    2. Импорт данных из Export.csv в базу данных (read_csv)

    Args:
        None

    Returns:
        None
    """
    review_test =  {
         'market_id': '1018261',
         'review_date': '2026-07-22 19:20:04.439247',
         'review_text': '',
         'score': '5',
         'user_id': 'ab80d15b-14e7-442d-8403-b6cc3242144a'}
    requiredFiles.prepare_refs()
    requiredFiles.create_market_table()
    requiredFiles.create_review_table()
    lst = filelib2.read_csv()
    datalib2.add_many(lst)
    n = Market.from_db(market_id=1018261)
    usr = User.from_db('sedart')
    r = Review(usr,n)
    r.set_score(5)
    r.set_text('this is text')
    r.save_to_db()
    n.calculate_score()
    n.banking_info.change_mode()
    get_markets_ordered_by_mode('num')
    get_all_markets_ordered_by_column(1)
    get_market_by_id(1018261)
    register_user()
    n.banking_info.change_mode()
    print('s')
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
            requiredFiles.create_user_table()
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
