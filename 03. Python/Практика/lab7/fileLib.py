"""
fileLib — библиотека для чтения данных о фермерских рынках.

Модуль парсит CSV-датасет Export.csv, создаёт справочники (MEDIA,
GROCERY_TYPES, BANKING_INFO, LOCATION) и связывает данные рынков
с элементами справочников через промежуточные CSV-файлы.

Использование:
    from fileLib import prepare_ref, read_csv
"""

import csv
import dataLib
from dataLib import create_reference, create_reference_entry

# Константы категорий для парсинга Export.csv
# Каждое множество определяет столбцы CSV-файла, относящиеся к данной категории.
ref_list = []  # Список справочников для инициализации через prepare_ref()
MARKET_INFO = {'MarketName', 'street', 'zip'}  # Основная информация о рынке

TIMESHEET_INFO = {'Season1Date',
                  'Season1Time',
                  'Season2Date',
                  'Season2Time',
                  'Season3Date',
                  'Season3Time',
                  'Season4Date',
                  'Season4Time'}  # Расписание по сезонам (дата + время)

COORDINATES = {'LON', 'LAT'}  # Географические координаты рынка

MEDIA = {
    'Website',
    'Facebook',
    'Twitter',
    'Youtube',
    'OtherMedia'
}  # Ссылки на сайты и соцсети рынка

LOCATION = {
    'city',
    'County',
    'State'
}  # Местоположение (город, округ, штат)

BANKING_INFO = {'Credit',
                'WIC',
                'WICcash',
                'SFMNP',
                'SNAP'}  # Принимаемые способы оплаты

GROCERY_TYPES = {'Organic',
         'Bakedgoods',
         'Cheese',
         'Crafts',
         'Flowers',
         'Eggs',
         'Seafood',
         'Herbs',
         'Vegetables',
         'Honey',
         'Jams',
         'Maple',
         'Meat',
         'Nursery',
         'Nuts',
         'Plants',
         'Poultry',
         'Prepared',
         'Soap',
         'Trees',
         'Wine',
         'Coffee',
         'Beans',
         'Fruits',
         'Grains',
         'Juices',
         'Mushrooms',
         'PetFood',
         'Tofu',
         'WildHarvested'}  # Типы товаров, реализуемых на рынке
ref_list.append({'MEDIA': MEDIA})
ref_list.append({'GROCERY_TYPES': GROCERY_TYPES})
ref_list.append({'BANKING_INFO': BANKING_INFO})


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
    for item in ref_list:
        ref_name = list(item.keys())[0]
        create_reference(ref_name)
        list_of_entries = item.get(ref_name)
        for value in list_of_entries:
            create_reference_entry(ref_name, value)

def read_csv():
    """
    Читает CSV-файл 'Export.csv' с данными о фермерских рынках.

    Парсит файл построчно, группирует информацию по рынкам (ключ — FMID)
    в словарь market_info и создаёт связи с справочниками.

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

    market_info = dict()
    count = 1679
    with open("Export.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            count -= 1
            print(f'Осталось {count} файлов')
            for key, value in row.items():
                if key == 'FMID':
                    current_id = value
                    market_info[current_id] = dict()
                if key in MARKET_INFO:
                    market_info[current_id][key.lower()] = value
                if key in COORDINATES:
                    market_info[current_id][key.lower()] = value
                if key in TIMESHEET_INFO:
                    market_info[current_id][key.lower()] = value
                if key in MEDIA:
                    reference_id = dataLib.read_reference_entry('MEDIA',entry_name=key)
                    dataLib.create_connection_entry("MarketXSocialMedia",current_id,reference_id[0], value)
                if key in GROCERY_TYPES:
                    reference_id = dataLib.read_reference_entry('GROCERY_TYPES', entry_name=key)
                    dataLib.create_connection_entry("MarketXGrocery", current_id, reference_id[0], value)
                if key in BANKING_INFO:
                    reference_id = dataLib.read_reference_entry('BANKING_INFO', entry_name=key)
                    dataLib.create_connection_entry("MarketXBankingInfo", current_id, reference_id[0], value)
                if key in LOCATION:
                    reference_id = dataLib.read_reference_entry(key.upper(), entry_name=value)
                    if reference_id == None:
                        create_reference_entry(key.upper(), value)
                        reference_id = dataLib.read_reference_entry(key.upper(), entry_name=value)
                        market_info[current_id][key.lower()] = reference_id[0]
                    else:
                        market_info[current_id][key.lower()] = reference_id[0]
        return(market_info)

