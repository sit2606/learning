"""
marketList — бизнес-логика для работы со списком рынков.

Модуль предоставляет функции для получения и сортировки данных
о фермерских рынках из MARKET_INFO.csv:

- get_all_markets(): все рынки с резолвингом ID → имена
- get_all_markets_ordered_by_num(): с порядковой нумерацией
- get_all_markets_ordered_by_column(col, order): сортировка по колонке
- prepare_ordered_list(markets): переиндексация для пагинации

Использование:
    from BusinessLogic.marketList import get_all_markets, get_all_markets_ordered_by_num
"""

from DAL.fileLib import get_markets_base
from DAL.referenceLib import  get_reference_with_uid_as_key


def get_all_markets():
    """
    Получает данные о всех фермерских рынках.

    Вызывает fileLib.get_markets_base() для чтения MARKET_INFO.csv.

    Returns:
        csv.DictReader: объект чтения CSV с данными о рынках.
    """
    market_base = get_markets_base()
    city_reference = get_reference_with_uid_as_key('CITY', 'Common')
    county_reference = get_reference_with_uid_as_key('COUNTY', 'Common')
    state_reference = get_reference_with_uid_as_key('STATE', 'Common')
    num  = 1
    for market_id, market_info in market_base.items():
        city = city_reference[market_info['city']]
        county = county_reference[market_info['county']]
        state = state_reference[market_info['state']]
        market_info.update({'city': city, 'county': county, 'state': state})
        market_info.update({'number': num})
        market_info.update({'market_id': market_id})
        num += 1
        market_base.update({market_id: market_info})
    return market_base
def get_all_markets_ordered_by_num():
    """
    Получает данные о всех фермерских рынках с порядковой нумерацией.

    Возвращает dict, где ключ — порядковый номер (int), значение — dict с атрибутами рынка.
    Используется для пагинации в команде 'list'.

    Returns:
        dict: словарь {номер: {атрибуты_рынка, number, market_id}}.
    """
    market_base = get_markets_base()
    city_reference = get_reference_with_uid_as_key('CITY', 'Common')
    county_reference = get_reference_with_uid_as_key('COUNTY', 'Common')
    state_reference = get_reference_with_uid_as_key('STATE', 'Common')
    num  = 1
    ordered_market_base = {}
    for market_id, market_info in market_base.items():
        city = city_reference[market_info['city']]
        county = county_reference[market_info['county']]
        state = state_reference[market_info['state']]
        market_info.update({'city': city, 'county': county, 'state': state})
        market_info.update({'number': num})
        market_info.update({'market_id': market_id})
        ordered_market_base.update({num: market_info})
        num += 1
    return ordered_market_base
def get_all_markets_ordered_by_column(column_number, order = False):
    """
    Получает данные о всех фермерских рынках, отсортированные по полю County.

    Сначала получает все рынки через get_all_markets(), затем сортирует
    по алфавиту по названию округа (County).

    Returns:
        dict: словарь {market_id: {атрибуты_рынка}}, отсортированный по County.
    """
    columns = {1 : 'number',
               2 : 'market_id',
               3 : 'city',
               4 : 'county',
               5 : 'state',
               6 : 'marketname',
               7 : 'zip'
               }
    match order:
        case 'a':
            order = False
        case 'd':
            order = True
    market_base = get_all_markets_ordered_by_num()
    sorting_base = {}
    for market_id, market_info in market_base.items():
        sorting_base.update({market_id: market_info[columns[column_number]] })
    sorted_items = sorted(sorting_base.items(), key=lambda x: x[1], reverse=order)
    ordered_market_base = dict()
    for item_id in sorted_items:
        ordered_market_base.update({item_id[0]: market_base[item_id[0]]})
    return ordered_market_base, columns[column_number]
def prepare_ordered_list(markets):
    markets_for_show = dict()
    for index, (key, value) in enumerate(markets.items(), start = 1):
        markets_for_show.update({index: value})
    return markets_for_show
