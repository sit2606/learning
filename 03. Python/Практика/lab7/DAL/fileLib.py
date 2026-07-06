"""
fileLib — библиотека для инициализации данных и парсинга CSV.

Модуль предоставляет функции для:
- Инициализации справочников (MEDIA, GROCERY_TYPES, BANKING_INFO)
- Парсинга Export.csv с батчевой записью связей
- Проверки наличия необходимых файлов
- Создания и чтения MARKET_INFO.csv
- Создания USER_INFO.csv
- Создания REVIEWS.csv
- Создания Reference_Base.csv (итоговый справочник всех справочников)

Операции со справочниками делегируются в referenceLib.
Все файлы хранятся в папке files/.

Использование:
    from DAL.fileLib import prepare_ref, read_csv, file_status_check, create_reference_base
"""

import csv
import uuid

from DAL import referenceLib, requiredFiles
from DAL.referenceLib import create_reference_entry, get_reference_with_name_as_key, create_connection_entry_by_list
import os

REF_LIST = [{'MEDIA': requiredFiles.MEDIA}, {'GROCERY_TYPES': requiredFiles.GROCERY_TYPES},
            {'BANKING_INFO': requiredFiles.BANKING_INFO}]  # Список справочников для инициализации через prepare_ref()


def prepare_ref():
    """
    Инициализирует справочники, создавая CSV-файлы и заполняя их данными.

    Перебирает элементы ref_list, для каждого справочника вызывает
    create_reference() для создания файла и create_reference_entry()
    для добавления всех значений из множества.

    Args:
        None

    Returns:
        None

    Example:
        >>> prepare_ref()
        # Создаёт файлы MEDIA.csv, GROCERY_TYPES.csv, BANKING_INFO.csv
        # и заполняет их записями
    """
    for item in REF_LIST:
        ref_name = list(item.keys())[0]
        referenceLib.create_reference(ref_name)
        list_of_entries = item.get(ref_name)
        for value in list_of_entries:
            create_reference_entry(ref_name, value)
def read_csv():
    """
    Читает CSV-файл 'Export.csv' с данными о фермерских рынках.

    Парсит файл построчно, группирует информацию по рынкам (ключ — FMID)
    в словарь market_info и создаёт связи со справочниками.

    Обрабатываемые категории:
    - MARKET_INFO → market_info: название, улица, индекс
    - COORDINATES → market_info: долгота, широта
    - TIMESHEET_INFO → market_info: расписание по сезонам
    - MEDIA → MarketXSocialMedia.csv: ссылки на соцсети
    - GROCERY_TYPES → MarketXGrocery.csv: типы товаров
    - BANKING_INFO → MarketXBankingInfo.csv: способы оплаты
    - LOCATION → CITY/COUNTY/STATE.csv: справочники местоположений

    Для столбцов MEDIA, GROCERY_TYPES, BANKING_INFO ищет reference_id
    в соответствующем справочнике и создаёт связь. Для LOCATION
    справочники создаются автоматически при первом добавлении нового значения.

    Args:
        None

    Returns:
        dict: словарь {FMID: {атрибуты_рынка}} со всей информацией о рынках.

    Raises:
        FileNotFoundError: если файл 'Export.csv' не найден.
        csv.Error: при ошибке парсинга CSV.

    Note:
        Выводит в консоль прогресс обработки (оставшееся кол-во строк).
        Файл 'Export.csv' должен находиться в текущей рабочей директории.
    """
    media_reference = get_reference_with_name_as_key('MEDIA', 'Common')
    grocery_types = get_reference_with_name_as_key('GROCERY_TYPES', 'Common')
    banking_info = get_reference_with_name_as_key('BANKING_INFO', 'Common')
    MarketXSocialMedia = []
    MarketXGrocery = []
    MarketXBankingInfo = []
    market_info = dict()
    count = 1679
    with open("Export.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            count -= 1
            print(f'Осталось {count} строк')
            for key, value in row.items():
                if key == 'FMID':
                    current_id = value
                    market_info[current_id] = dict()
                if key in requiredFiles.MARKET_INFO:
                    market_info[current_id][key.lower()] = value
                if key in requiredFiles.COORDINATES:
                    market_info[current_id][key.lower()] = value
                if key in requiredFiles.TIMESHEET_INFO:
                    market_info[current_id][key.lower()] = value
                if key in requiredFiles.MEDIA:
                    reference_id = media_reference[key]
                    MarketXSocialMedia.append([current_id, reference_id, value])
                if key in requiredFiles.GROCERY_TYPES:
                    reference_id = grocery_types[key]
                    MarketXGrocery.append([current_id, reference_id, value])
                if key in requiredFiles.BANKING_INFO:
                    reference_id = banking_info[key]
                    MarketXBankingInfo.append([current_id, reference_id, value])
                if key in requiredFiles.LOCATION:
                    reference_id = referenceLib.read_reference_entry(key.upper(), entry_name=value)
                    if reference_id is None:
                        create_reference_entry(key.upper().strip(), value)
                        reference_id = referenceLib.read_reference_entry(key.upper(), entry_name=value)
                        market_info[current_id][key.lower()] = reference_id[0]
                    else:
                        market_info[current_id][key.lower()] = reference_id[0]
                market_info[current_id]['score'] = None
        create_connection_entry_by_list('MarketXSocialMedia',MarketXSocialMedia)
        create_connection_entry_by_list('MarketXGrocery', MarketXGrocery)
        create_connection_entry_by_list('MarketXBankingInfo', MarketXBankingInfo)
        return market_info
def file_status_check():
    """
    Проверяет наличие всех необходимых CSV-файлов в текущей директории.

    Перебирает имена из requiredFiles.FILES_TO_CHECK и проверяет
    существование каждого файла. Выводит в консоль список отсутствующих файлов.

    Returns:
        bool: True если хотя бы один файл отсутствует (требуется пересоздание),
              False если все файлы на месте.
    """
    creation_needed = False
    for file in requiredFiles.FILES_TO_CHECK:
        file_path = f"files/{file}.csv"
        if not os.path.isfile(file_path):
            print(f'No {file}.csv in directory')

            creation_needed = True
    if creation_needed:
        print('Files will be recreated from Exports.csv')

    else:
        print('No recreation needed')
    return creation_needed
def create_market_base(market_info):
    """
    Создаёт CSV-файл MARKET_INFO.csv с расширенной информацией о рынках.

    Принимает словарь market_info (возвращённый read_csv()) и записывает
    данные в CSV-файл со структурой: market_id, market_name, street, city,
    county, state, zip, season1date-time, season2date-time, season3date-time, season4date-time.

    Args:
        market_info (dict): Словарь {FMID: {атрибуты_рынка}} из read_csv().

    Returns:
        None

    Raises:
        Exception: при ошибке записи файла выводит сообщение
        "Error in create market base" и текст исключения в консоль.
    """
    _reference_name = 'MARKET_INFO'
    field_names = ['market_id',
                   'marketname',
                   'street',
                   'city',
                   'county',
                   'state',
                   'zip',
                   'season1date',
                   'season1time',
                   'season2date',
                   'season2time',
                   'season3date',
                   'season3time',
                   'season4date',
                   'season4time',
                   'score']
    try:
        with open(f"files/{_reference_name}.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            for i in market_info:
                row = {'market_id':i}
                row.update(market_info[i])
                writer.writerow(row)
    except Exception as e:
        print(e)
        print("Error in create market base")
def create_user_base():
    """
    Создаёт CSV-файл USER_INFO.csv с заголовками для хранения данных пользователей.

    Структура файла: Id, user_name, password, firstname, lastname, location.

    Raises:
        Exception: при ошибке создания файла выводит сообщение
        "Error in create_user_base" и текст исключения в консоль.
    """
    _reference_name = 'USER_INFO'
    field_names = ['Id',
                   'user_name',
                   'password',
                   'firstname',
                   'lastname',
                   'location']
    try:
        with open(f"files/{_reference_name}.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
    except Exception as e:
        print(e)
        print("Error in create_user_base")
def get_raw_markets_from_file():
    """
    Читает CSV-файл MARKET_INFO.csv и возвращает данные о рынках.

    Returns:
        dict: словарь {market_id: {атрибуты_рынка}}.

    Raises:
        Exception: при ошибке чтения файла выводит сообщение
        "Error in get_raw_markets_from_file".
    """
    _reference_name = 'MARKET_INFO'
    market_base = dict()
    try:
        with open(f"files/{_reference_name}.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for market_info in reader:
                market_id = market_info['market_id']
                market_info.pop('market_id')
                market_base.update({market_id: market_info})
        return  market_base
    except Exception as e:
        print(e)
        print("Error in get_raw_markets_from_file")


def create_reference_base():
    """
    Создаёт CSV-файл Reference_Base.csv со списком всех справочников.

    Файл содержит заголовки: ID, Reference_Name.
    Записывает имя каждого справочника из FILES_TO_CHECK с уникальным UUID.

    Raises:
        Exception: при ошибке выводит "Error in create_reference_base".
    """
    try:
        with open(f"files/{'Reference_Base'}.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=['ID','Reference_Name'])
            writer.writeheader()
            for reference_name in requiredFiles.FILES_TO_CHECK:
                uid = uuid.uuid4()
                writer.writerow({'ID': uid, 'Reference_Name': reference_name})
    except Exception as e:
        print(e)
        print("Error in create_reference_base")
def create_review_base():
    """
    Создаёт CSV-файл REVIEWS.csv с заголовками для хранения отзывов.

    Структура файла: Id, review_date, user_id, market_id, review_text, score.

    Raises:
        Exception: при ошибке создания файла выводит сообщение
        "Error in create_review_base" и текст исключения в консоль.
    """
    _reference_name = 'REVIEWS'
    field_names = ['Id',
                   'review_date',
                   'user_id',
                   'market_id',
                   'review_text',
                   'score']
    try:
        with open(f"files/{_reference_name}.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
    except Exception as e:
        print(e)
        print("Error in create_review_base")