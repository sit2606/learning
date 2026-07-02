"""
workflowLib — модуль оркестрации рабочего процесса и обработки команд.

Связывает создание директории для файлов, проверку наличия файлов,
инициализацию справочников, парсинг данных, обработку пользовательских
команд и вывод результатов в консоль.

Использование:
    from BusinessLogic.workflowLib import directory_creation, file_creation, get_command, proceed_command
"""
import os

from BusinessLogic import commandHandler
from DAL import fileLib
from UI import uiLib


def directory_creation():
    """
    Создаёт папку 'files/' для хранения CSV-файлов.

    Использует os.makedirs() с exist_ok=True для безопасного создания.

    Raises:
        Exception: при ошибке создания директории выводит сообщение
        "Error in directory_creation" и текст исключения в консоль.
    """
    try:
        os.makedirs("../files", exist_ok=True)
    except Exception as e:
        print(e)
        print("Error in directory_creation")
def file_creation():
    """
    Проверяет наличие необходимых CSV-файлов и пересоздаёт данные при необходимости.

    1. Вызывает fileLib.file_status_check() для проверки наличия файлов
    2. Если файлы отсутствуют — инициализирует справочники через fileLib.prepare_ref()
    3. Читает Export.csv и создаёт MARKET_INFO.csv через fileLib.create_market_base()
    4. Создаёт USER_INFO.csv через fileLib.create_user_base()
    """
    if fileLib.file_status_check():
        print('Recreation in progress...')
        print('Creating basic refs...')
        fileLib.prepare_ref()
        print('Basic refs created...')
        print('Exporting MARKET_INFO.csv...')
        fileLib.create_market_base(fileLib.read_csv())
        print('MARKET_INFO.csv exported, all important files successfully created...')
        print('User base recreation in progress...')
        fileLib.create_user_base()
        print('User base successfully created...')

def get_command():
    command = input('Пожалуйста, введите команду: ')
    return command
def proceed_command(command):
    is_run = True
    match command:
        case 'help':
            uiLib.print_help()
            is_run = commandHandler.command_help()
        case 'list':
            is_run, market_list = commandHandler.command_list()
            uiLib.print_list(market_list)
        case 'exit':
            uiLib.print_exit()
            is_run = commandHandler.command_exit()
    return is_run
