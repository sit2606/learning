"""
requiredFiles — константы категорий для парсинга Export.csv и список файлов для проверки.

Модуль содержит множества столбцов CSV-файла, сгруппированные по категориям:
- MARKET_INFO, COORDINATES, TIMESHEET_INFO — основная информация о рынках
- MEDIA, LOCATION, BANKING_INFO, GROCERY_TYPES — справочники

Также содержит FILES_TO_CHECK — множество имён CSV-файлов для проверки наличия.

Использование:
    from DAL.requiredFiles import MARKET_INFO, MEDIA, FILES_TO_CHECK
"""


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