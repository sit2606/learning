"""
workflowLib — модуль оркестрации рабочего процесса.

Зависимости:
- os: работа с файловой системой
- BusinessLogic.commandHandler: обработчики команд
- DAL.requiredFiles: инициализация таблиц и справочников
- DAL.filelib2: импорт CSV в SQLite
- DAL.datalib2: batch-вставка рынков
- view.uiLib: вывод в консоль
- models.entities.user.User: сущность пользователя

Основные функции:
- directory_creation(): создание папки files/
- file_creation(): проверка и пересоздание CSV-файлов
- get_command(user): ввод команды от пользователя (с приветствием для авторизованных)
- proceed_command(command, user): маршрутизация и выполнение команды

Поддерживаемые команды:
- help — справка
- list_all — все рынки
- list — список с пагинацией
- order — сортировка по колонке
- show — данные одного рынка по Id (с просмотром отзывов)
- filter — фильтрация рынков по колонке
- register — регистрация пользователя (с запросом координат)
- login — авторизация пользователя
- logout — выход из системы
- review — добавление отзыва
- update_user — обновление данных пользователя
- delete — удаление рынка и его связей
- zip — поиск рынков в радиусе от почтового индекса
- exit — выход

Использование:
    from BusinessLogic.workflowLib import directory_creation, file_creation, proceed_command
"""
import os

from controller import commandHandler
from DAL import  requiredFiles, filelib2, datalib2

from view import uiLib
from models.entities.user import User


def directory_creation():
    """
    Создаёт папку 'files/' для хранения CSV-файлов.

    Использует os.makedirs() с exist_ok=True для безопасного создания.

    Raises:
        Exception: при ошибке создания директории выводит сообщение
        "Error in directory_creation" и текст исключения в консоль.
    """
    try:
        os.makedirs("files", exist_ok=True)
    except Exception as e:
        print(e)
        print("Error in directory_creation")
def file_creation():
    """Инициализирует таблицы и заполняет базу данных из CSV.

    Создаёт справочники, таблицы MARKETS/REVIEWS/USERS,
    импортирует данные из Export.csv и заполняет MARKETS.
    """
    requiredFiles.prepare_refs()
    requiredFiles.create_market_table()
    requiredFiles.create_review_table()
    requiredFiles.create_user_table()
    datalib2.add_many(filelib2.read_csv())
def get_command(user):
    """
    Считывает команду пользователя из stdin.

    Если пользователь авторизован — выводит приветствие с именем.
    Если не авторизован — выводит предупреждение о недоступных функциях.

    Args:
        user: Текущий авторизованный пользователь или None.

    Returns:
        str: введённая пользователем команда.
    """
    command =  commandHandler.get_command(user)
    return command
def proceed_command(command, user):
    """
    Обрабатывает команду пользователя и возвращает состояние сессии.

    Args:
        command: Строка команды от пользователя.
        user: Текущий авторизованный пользователь или None.

    Returns:
        (is_run, user) — кортеж (продолжать ли работу, текущий пользователь).
    """
    is_run = True
    match command:
        case 'help':
            is_run = commandHandler.command_help()
        case 'list_all':
            is_run = commandHandler.command_list_all()
        case 'list':
            is_run= commandHandler.command_list()
        case 'order':
            is_run = commandHandler.command_order()
        case 'show':
            is_run = commandHandler.command_show()
        case 'register':
            is_run, user = commandHandler.register_user()
        case 'login':
            is_run, user = commandHandler.login_user(user)
        case 'logout':
            is_run, user = commandHandler.logout_user(user)
        case 'review':
            is_run, user = commandHandler.add_review(user)
        case 'update_user':
            is_run, user = commandHandler.update_user(user)
        case 'filter':
            is_run, user = commandHandler.show_filtered(user)
        case 'delete':
            is_run, user = commandHandler.delete_market(user)
        case 'exit':
            is_run = commandHandler.command_exit()
        case 'zip':
            is_run = commandHandler.command_zip()
        case _:
            is_run = commandHandler.unknown_command()
    return is_run, user
