"""
fileLib — библиотека для работы с CSV-справочниками и данными о фермерских рынках.

Модуль предоставляет функции для создания, чтения и обновления CSV-файлов,
а также для парсинга датасета фермерских рынков (FMSS/Export.csv).

Использование:
    from fileLib import read_csv, update_reference_entry
"""

import csv
import uuid

# Константы категорий для парсинга Export.csv
# Каждое множество определяет столбцы CSV-файла, относящиеся к данной категории.

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

GOODS = {'Organic',
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
def read_csv():
    """
    Читает CSV-файл 'Export.csv' с данными о фермерских рынках (FMSS dataset).

    Парсит файл построчно и группирует информацию по рынкам (ключ — FMID)
    в словарь market_info. Каждый рынок распределяется по категориям,
    определённым на уровне модуля:

    - MARKET_INFO — название рынка, улица, почтовый индекс
    - COORDINATES — долгота (LON) и широта (LAT)
    - TIMESHEET_INFO — расписание работы по 4 сезонам (дата + время)
    - MEDIA — ссылки на сайт, Facebook, Twitter, Youtube, прочие медиа
    - LOCATION — город, округ (County), штат (State)
    - BANKING_INFO — принимаемые способы оплаты (Credit, WIC, SNAP и др.)
    - GOODS — типы товаров (Organic, Vegetables, Honey, Meat и др.)

    Args:
        None

    Returns:
        None. Результат накапливается в локальном словаре market_info
        и выводится в консоль по ходу выполнения.

    Raises:
        FileNotFoundError: если файл 'Export.csv' не найден.
        csv.Error: при ошибке парсинга CSV.

    Note:
        - Файл 'Export.csv' должен находиться в текущей рабочей директории.
        - Функция содержит незавершённый блок обработки MEDIA (строка ~142).
    """

    market_info = dict()
    with open("Export.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key, value in row.items():
                print('a')
                if key == 'FMID':
                    current_id = value
                    market_info[current_id] = dict()
                if key in MARKET_INFO:
                    market_info[current_id][key] = value
                if key in COORDINATES:
                    market_info[current_id][key] = value
                if key in TIMESHEET_INFO:
                    market_info[current_id][key] = value
                if key in MEDIA:

    print('a')

