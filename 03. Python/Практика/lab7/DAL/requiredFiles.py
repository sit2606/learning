"""
requiredFiles — константы категорий для парсинга Export.csv и список файлов для проверки.

Модуль содержит множества столбцов CSV-файла, сгруппированные по категориям:
- MARKET_INFO, COORDINATES, TIMESHEET_INFO — основная информация о рынках
- MEDIA, LOCATION, BANKING_INFO, GROCERY_TYPES — справочники

Также содержит FILES_TO_CHECK — множество имён CSV-файлов для проверки наличия.

Использование:
    from DAL.requiredFiles import MARKET_INFO, MEDIA, FILES_TO_CHECK
"""
import sqlite3

from config import DATABASE_PATH
from models.entities.reference import Reference

MARKET_INFO = {'MarketName'}  # Основная информация о рынке

TIMESHEET_INFO = {'Season1Date',
                  'Season1Time',
                  'Season2Date',
                  'Season2Time',
                  'Season3Date',
                  'Season3Time',
                  'Season4Date',
                  'Season4Time'}  # Расписание по сезонам (дата + время)

COORDINATES = {'x', 'y'}  # Географические координаты рынка

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
    'State',
    'street',
    'zip'
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

FILES_TO_CHECK = {
    'BANKING_INFO',
    'CITY',
    'COUNTY',
    'GROCERY_TYPES',
    'MARKET_INFO',
    'MarketXBankingInfo',
    'MarketXGrocery',
    'MarketXSocialMedia',
    'MEDIA',
    'STATE',
    'USER_INFO',
    'REVIEWS'
}
# Множество имён CSV-файлов (без расширения) для проверки наличия перед работой
REF_LIST = {'required_refs': {
                              'MEDIA':'Common',
                              'GROCERY_TYPES': 'Common',
                              'BANKING_INFO': 'Common',
                              'CITY': 'Common',
                              'COUNTY': 'Common',
                              'STATE': 'Common',
                              'MarketXSocialMedia': 'Connection',
                              'MarketXGrocery' : 'Connection',
                              'MarketXBankingInfo': 'Connection'
                                },
            'values':           {
                            'MEDIA': MEDIA,
                            'GROCERY_TYPES': GROCERY_TYPES,
                            'BANKING_INFO': BANKING_INFO
                                }
            }



def prepare_refs():
    """
    Инициализирует справочники в SQLite.

    Создаёт таблицы для всех справочников из REF_LIST['required_refs'],
    затем заполняет простые справочники записями из REF_LIST['values'].

    Returns:
        None
    """
    for item in REF_LIST['required_refs'].items():
        ref = Reference(item[0], item[1])
    for item in REF_LIST['values'].items():
        ref = Reference(item[0])
        for entry in item[1]:
            ref.add(entry)
def create_user_table():
    """
    Создаёт таблицу USERS в SQLite (если не существует).

    Структура таблицы: id, username, password, firstname, lastname, latitude, longitude.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS USERS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password text NOT NULL,
            firstname text NOT NULL,
            lastname text NOT NULL,
            latitude real,
            longitude real
        )''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        print("Error in create_user_table")
def create_market_table():
    """
    Создаёт таблицу MARKETS в SQLite (если не существует).

    Структура таблицы: id, marketname, street, city, county, state, zip,
    longitude, latitude, season1-4date/time, score.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS MARKETS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marketname TEXT NOT NULL,
            street TEXT NOT NULL,
            city TEXT NOT NULL,
            county TEXT NOT NULL,
            state TEXT NOT NULL,
            zip TEXT NOT NULL,
            longitude REAL,
            latitude REAL,
            season1date TEXT,
            season1time TEXT,
            season2date TEXT,
            season2time TEXT,
            season3date TEXT,
            season3time TEXT,
            season4date TEXT,
            season4time TEXT,
            score REAL
        )''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        print("Error in create_market_table")
def create_review_table():
    """
    Создаёт таблицу REVIEWS в SQLite (если не существует).

    Структура таблицы: id, review_date, user_id, market_id, review_text, score.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS REVIEWS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review_date TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            market_id INTEGER NOT NULL,
            review_text TEXT,
            score REAL
        )''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        print("Error in create_review_table")