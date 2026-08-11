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
import sys
from UI.table_view import MainWindow
from PyQt5.QtWidgets import QApplication

def testing():
    """Тестирование OOP-функций SQLite.

    Выполняет:
    1. Инициализацию справочных таблиц (prepare_refs)
    2. Создание таблиц MARKETS, REVIEWS
    3. Импорт данных из Export.csv (read_csv + add_many)
    4. Тестирование Market.from_db() — загрузка рынка со справочниками
    5. Тестирование Review — создание и сохранение отзыва
    6. Тестирование Market.calculate_score() — пересчёт оценки
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
    1. file_creation() — инициализация таблиц и импорт данных из CSV
    2. Цикл команд: приветствие, чтение и обработка команд
       с отслеживанием текущего пользователя (user = None при старте)
    """
   # testing()
    file_creation()
    run_app = True
    print_welcome()
    user = None
    run_gui()
    while run_app:
        command = get_command(user)
        run_app, user = proceed_command(command, user)

def run_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()

