"""
Модуль инициализации справочных данных и импорта CSV в SQLite (версия 2).

Содержит функции:
    - prepare_ref() — создание и заполнение справочных таблиц (MEDIA, GROCERY_TYPES, BANKING_INFO)
    - read_csv() — импорт данных из Export.csv в базу данных

Справочники:
    - MEDIA: типы СМИ
    - GROCERY_TYPES: типы продовольственных товаров
    - BANKING_INFO: банковские реквизиты
    - CITY, COUNTY, STATE: справочники местоположений (создаются автоматически)
"""

from DAL import requiredFiles
from DAL.referencelib2 import get_reference_with_name_as_key, create_connection_entry_by_list,  create_reference_entry_by_list
import csv
def read_csv():
    """
    Читает CSV-файл 'Export.csv' с данными о фермерских рынках.

    Парсит файл построчно, группирует информацию по рынкам (ключ — FMID)
    в словарь market_info и создаёт связи со справочниками.

    Алгоритм:
    1. Загружает справочники MEDIA, GROCERY_TYPES, BANKING_INFO в память
    2. Читает CSV, собирает уникальные значения CITY/COUNTY/STATE в set
    3. Создаёт таблицы CITY/COUNTY/STATE и batch-вставляет значения
    4. Заменяет текстовые значения на ID из справочников
    5. Создаёт связующие таблицы и batch-вставляет связи

    Обрабатываемые категории:
    - MARKET_INFO → market_info: название, улица, индекс
    - COORDINATES → market_info: долгота, широта
    - TIMESHEET_INFO → market_info: расписание по сезонам
    - MEDIA → связь рынков с соцсетями
    - GROCERY_TYPES → связь рынков с типами товаров
    - BANKING_INFO → связь рынков с способами оплаты
    - LOCATION → CITY/COUNTY/STATE: справочники местоположений

    Args:
        None

    Returns:
        dict: словарь {FMID: {атрибуты_рынка}} со всей информацией о рынках.
              Включает: name, street, zip, longitude, latitude, schedule,
                        city (ID), county (ID), state (ID), score, distance

    Raises:
        FileNotFoundError: если файл 'Export.csv' не найден.
        csv.Error: при ошибке парсинга CSV.

    Note:
        Файл 'Export.csv' должен находиться в текущей рабочей директории.
        Таблицы CITY, COUNTY, STATE создаются автоматически при первом запуске.
    """
    media_reference = get_reference_with_name_as_key('MEDIA', 'Common')
    grocery_types = get_reference_with_name_as_key('GROCERY_TYPES', 'Common')
    banking_info = get_reference_with_name_as_key('BANKING_INFO', 'Common')
    MarketXSocialMedia = []
    MarketXGrocery = []
    MarketXBankingInfo = []
    cities = set()
    counties = set()
    states = set()
    location_dict = {
        'city': cities,
        'County': counties,
        'State': states
    }
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
                    if key == 'x':
                        if value.strip() == '':
                            value = '0'
                        market_info[current_id]['longitude'] = value
                    if key == 'y':
                        if value.strip() == '':
                            value = '0'
                        market_info[current_id]['latitude'] = value
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
                    value = value.strip().capitalize()
                    location_dict[key].add(value)
                    market_info[current_id][key.lower()] = value
                market_info[current_id]['score'] = None
                market_info[current_id]['distance'] = None
        create_reference_entry_by_list('CITY', [(item,) for item in location_dict['city']])
        create_reference_entry_by_list('COUNTY', [(item,) for item in location_dict['County']])
        create_reference_entry_by_list('STATE', [(item,) for item in location_dict['State']])
        location_dict['city'] = get_reference_with_name_as_key('CITY', 'Common')
        location_dict['County'] = get_reference_with_name_as_key('COUNTY', 'Common')
        location_dict['State'] = get_reference_with_name_as_key('STATE', 'Common')
        for key in market_info.keys():
            market_info[key]['city']  = location_dict['city'][market_info[key]['city']]
            market_info[key]['county'] = location_dict['County'][market_info[key]['county']]
            market_info[key]['state'] = location_dict['State'][market_info[key]['state']]
        create_connection_entry_by_list('MarketXSocialMedia',MarketXSocialMedia)
        create_connection_entry_by_list('MarketXGrocery', MarketXGrocery)
        create_connection_entry_by_list('MarketXBankingInfo', MarketXBankingInfo)
        return market_info
