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
import csv

from models.collections.market_collection import MarketCollection
from models.entities.market import Market
from models.entities.reference import Reference


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
            market.ref_mode = 'value'
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
        a = MarketCollection.from_dict(market_dict)
        a.change_mode()
        market_list = a.as_list()А 
        marketXsocial = Reference('MarketXSocialMedia', 'Connection')
        marketXgrocery = Reference('MarketXGrocery', 'Connection')
        marketXbankinginfo = Reference('MarketXBankingInfo', 'Connection')
        marketXsocial.add_many(MarketXSocialMedia)
        marketXgrocery.add_many(MarketXGrocery)
        marketXbankinginfo.add_many(MarketXBankingInfo)
        return market_list
