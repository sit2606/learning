"""
App — точка входа приложения для управления фермерскими рынками.

Создаёт AppController, инициализирует БД и запускает консольный UI.

Использование:
    python App.py
"""
from controller.AppController import AppController
from controller.workflow import run_console, run_gui


def main():
    """
    Основная функция запуска приложения.

    Порядок выполнения:
    1. Создание AppController (хранилище сессии + бизнес-логика)
    2. init_db() — инициализация таблиц и импорт данных из CSV
    3. run_console() — цикл обработки пользовательских команд
    """
    controller = AppController()
    controller.init_db()
    #run_console(controller)
    run_gui(controller)



if __name__ == "__main__":
    main()
