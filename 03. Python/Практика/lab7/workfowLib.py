"""
workfowLib — модуль оркестрации рабочего процесса.

Связывает создание директории для файлов, проверку наличия файлов,
инициализацию справочников и парсинг данных в единый рабочий процесс.

Использование:
    from workfowLib import directory_creation, file_creation
"""
import os

import fileLib
import dataLib


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