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

Алгоритм read_csv():
    1. Загружает справочники (MEDIA, GROCERY_TYPES, BANKING_INFO) для сопоставления имён → ID
    2. Читает Export.csv построчно, для каждой строки (рынка):
       - Создаёт объект Market с market_info, timesheet, coordinates, location
       - Заполняет поля через setattr() на основе ключей CSV
       - Собирает связи many-to-many (SocialMedia, Grocery, BankingInfo)
       - Собирает уникальные значения городов, округов, штатов, почтовых индексов, улиц
    3. Сохраняет справочники местоположений в БД и получает их ID
    4. Заменяет строковые значения локаций на ID из справочников
    5. Сохраняет связи many-to-many в промежуточные таблицы
    6. Возвращает список объектов Market с заполненными ID

Особенности:
    - Использует Reference class для работы со справочниками
    - Значения координат приводятся к float (пустые строки → 0.0)
    - Значения локаций приводятся к Capitalized виду
"""

from DAL import requiredFiles
import csv

from models.market import Market
from models.reference import Reference


def read_csv():
    """
    Импортирует данные из CSV-файла Export.csv в базу данных SQLite.

    Функция выполняет полный цикл импорта:
    - Загружает справочники (MEDIA, GROCERY_TYPES, BANKING_INFO) для маппинга
    - Парсит CSV-файл, создавая объекты Market для каждой строки
    - Заполняет промежуточные таблицы связей (MarketXSocialMedia, MarketXGrocery, MarketXBankingInfo)
    - Создаёт и заполняет справочники локаций (CITY, COUNTY, STATE, ZIP, STREET)
    - Заменяет строковые значения локаций на ID из справочников

    Возвращает:
        list[Market]: Список объектов Market с заполненными полями и связями.

    Примечания:
        - Файл Export.csv должен находиться в рабочей директории
        - Пустые значения координат заменяются на 0.0
        - Значения локаций приводятся к Capitalized виду (первая заглавная)
        - Промежуточные таблицы связей заполняются после основного цикла
    """

    media = Reference('MEDIA')
    grocery = Reference('GROCERY_TYPES')
    banking = Reference('BANKING_INFO')
    media_reference = media.get_all_with_names()
    grocery_types = grocery.get_all_with_names()
    banking_info = banking.get_all_with_names()
    MarketXSocialMedia = []
    MarketXGrocery = []
    MarketXBankingInfo = []
    cities = set()
    counties = set()
    states = set()
    zip = set()
    street = set()
    location_dict :dict[str, set] = {
        'city': cities,
        'County': counties,
        'State': states,
        'zip' : zip,
        'street' : street,
    }
    market_dict = dict()
    count = 1679
    with (open("Export.csv", newline="") as csvfile):
        reader = csv.DictReader(csvfile)
        for row in reader:
            count -= 1
            print(f'Осталось {count} строк')
            for key, value in row.items():
                if key == 'FMID':
                    current_id = value
                    market = Market(current_id)
                if key in requiredFiles.MARKET_INFO:
                    if hasattr(market.market_info, key.lower()):
                        setattr(market.market_info, key.lower(), value)
                if key in requiredFiles.COORDINATES:
                    if key == 'x':
                        if value.strip() == '':
                            value = '0'
                        market.coordinates.longitude = float(value)
                    if key == 'y':
                        if value.strip() == '':
                            value = '0'
                        market.coordinates.latitude = float(value)
                if key in requiredFiles.TIMESHEET_INFO:
                    if hasattr(market.timesheet, key.lower()):
                        setattr(market.timesheet, key.lower(), value)
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
                    if hasattr(market.location, key.lower()):
                        setattr(market.location, key.lower(), value)
            market_dict[current_id] = market
        city = Reference('CITY')
        county = Reference('COUNTY')
        state = Reference('STATE')
        zip = Reference('ZIP')
        street = Reference('STREET')
        city.add_many([(item,) for item in location_dict['city']])
        county.add_many([(item,) for item in location_dict['County']])
        state.add_many([(item,) for item in location_dict['State']])
        zip.add_many([(item,) for item in location_dict['zip']])
        street.add_many([(item,) for item in location_dict['street']])
        location_dict['city'] =city.get_all_with_names()
        location_dict['County'] =county.get_all_with_names()
        location_dict['State'] = state.get_all_with_names()
        location_dict['Zip'] = zip.get_all_with_names()
        location_dict['street'] = street.get_all_with_names()
        market_list =[]
        for key in market_dict.keys():
            market_dict[key].location.city  = location_dict['city'][market_dict[key].location.city]
            market_dict[key].location.county  = location_dict['County'][market_dict[key].location.county]
            market_dict[key].location.state = location_dict['State'][market_dict[key].location.state]
            market_dict[key].location.zip = location_dict['Zip'][market_dict[key].location.zip]
            market_dict[key].location.street = location_dict['street'][market_dict[key].location.street]
            market_list.append(market_dict[key])
        marketXsocial = Reference('MarketXSocialMedia', 'Connection')
        marketXgrocery = Reference('MarketXGrocery', 'Connection')
        marketXbankinginfo = Reference('MarketXBankingInfo', 'Connection')
        marketXsocial.add_many(MarketXSocialMedia)
        marketXgrocery.add_many(MarketXGrocery)
        marketXbankinginfo.add_many(MarketXBankingInfo)
        return market_list
