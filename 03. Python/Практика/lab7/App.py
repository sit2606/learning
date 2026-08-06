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


from UI.uiLib import print_welcome
from BusinessLogic.workflowLib import *
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
    print('s')


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
   # testing()
    file_creation()
    run_app = True
    print_welcome()
    user = None
    while run_app:
        command = get_command(user)
        run_app, user = proceed_command(command, user)


if __name__ == "__main__":
    main()
