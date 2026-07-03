"""
workflowLib — модуль оркестрации рабочего процесса и обработки команд.

Связывает создание директории для файлов, проверку наличия файлов,
инициализацию справочников, парсинг данных, обработку пользовательских
команд и вывод результатов в консоль.

Использование:
    from BusinessLogic.workflowLib import directory_creation, file_creation, get_command, proceed_command
"""
import os
from multiprocessing import context

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
    command = input('Пожалуйста, введите команду: ').strip()
    return command
def proceed_command(command):
    is_run = True
    match command:
        case 'help':
            uiLib.print_help()
            is_run = commandHandler.command_help()
        case 'list_all':
            is_run, market_list = commandHandler.command_list_all()
            if market_list is None:
                print('Ошибка. Попробуйте ещё раз')
            else:
                uiLib.print_list_all(market_list)
        case 'list':
            is_run, market_list, start_pos, step = commandHandler.command_list()
            if market_list is None:
                print('Ошибка. Попробуйте ещё раз')
            else:
                uiLib.print_list(markets_for_show= market_list,start_pos=start_pos, step= step)
        case 'order':
            uiLib.print_ordered_instruction()
            is_run, market_list, column, order = commandHandler.command_order()
            if market_list is None:
                print('Ошибка. Попробуйте ещё раз')
            else:
                ordered_list, position, step = uiLib.print_list(markets_for_show=market_list, column_name= column)
                is_continue = True
                while is_continue:
                    continue_command = input('Желаете продолжить? Введите \'y\' для продолжения, или \'n\' для завершения: ')
                    match continue_command:
                        case 'y':
                            ordered_list, position, step = uiLib.print_list(markets_for_show=ordered_list, column_name= column,
                                                                            step= step,start_pos=position)
                        case 'n':
                            is_continue = False
                        case _:
                            print('Ошибка ввода')
        case 'exit':
            uiLib.print_exit()
            is_run = commandHandler.command_exit()
        case _:
            print('Такой команды нет. Введите help, чтобы вывести список всех команд')
    return is_run
