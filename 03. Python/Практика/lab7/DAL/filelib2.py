"""
Модуль инициализации справочных данных в SQLite (версия 2).

Содержит функцию prepare_ref() для создания и заполнения справочных таблиц
при первом запуске приложения.

Справочники:
    - MEDIA: типы СМИ
    - GROCERY_TYPES: типы продовольственных товаров
    - BANKING_INFO: банковские реквизиты
"""

from DAL import requiredFiles, referencelib2
from DAL import referenceLib, requiredFiles
from DAL.referencelib2 import create_reference_entry, get_reference_with_name_as_key, create_connection_entry_by_list, \
    create_connection_reference
import csv
REF_LIST = [
    {'MEDIA': requiredFiles.MEDIA},
    {'GROCERY_TYPES': requiredFiles.GROCERY_TYPES},
    {'BANKING_INFO': requiredFiles.BANKING_INFO}
]


def prepare_ref():
    """Инициализирует справочники, создавая таблицы и заполняя их данными.

    Для каждого справочника:
    1. Создаёт таблицу (create_reference)
    2. Добавляет все значения из множества (create_reference_entry)

    Args:
        None

    Returns:
        None

    Example:
        >>> prepare_ref()
        # Создаёт таблицы MEDIA, GROCERY_TYPES, BANKING_INFO
        # и заполняет их записями из requiredFiles
    """
    for item in REF_LIST:
        ref_name = list(item.keys())[0]
        referencelib2.create_reference(ref_name)
        list_of_entries = item.get(ref_name)
        for value in list_of_entries:
            referencelib2.create_reference_entry(ref_name, value)
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
                    reference_id = referencelib2.read_reference_entry(key.upper(), entry_name=value)
                    if reference_id is None:
                        create_reference_entry(key.upper().strip(), value)
                        reference_id = referenceLib.read_reference_entry(key.upper(), entry_name=value)
                        market_info[current_id][key.lower()] = reference_id[0]
                    else:
                        market_info[current_id][key.lower()] = reference_id[0]
                market_info[current_id]['score'] = None
                market_info[current_id]['distance'] = None
        create_connection_reference('MarketXSocialMedia')
        create_connection_reference('MarketXGrocery')
        create_connection_reference('MarketXBankingInfo')
        create_connection_entry_by_list('MarketXSocialMedia',MarketXSocialMedia)
        create_connection_entry_by_list('MarketXGrocery', MarketXGrocery)
        create_connection_entry_by_list('MarketXBankingInfo', MarketXBankingInfo)
        return market_info