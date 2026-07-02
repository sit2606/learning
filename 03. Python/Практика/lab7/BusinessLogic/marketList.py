"""
marketList — бизнес-логика для работы со списком рынков.

Модуль предоставляет функцию get_all_markets() для получения
данных о фермерских рынках из CSV-файла MARKET_INFO.csv.

Использование:
    from BusinessLogic.marketList import get_all_markets
"""

from DAL.fileLib import get_markets_base
from DAL.referenceLib import get_reference_with_name_as_key, get_reference_with_uid_as_key


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
        market_info.number({'number': num})
        num += 1
        market_base.update({market_id: market_info})
    return market_base
def get_all_markets_ordered_by_num():
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



