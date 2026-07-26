"""
market_queries — запросы к данным о фермерских рынках.

Модуль содержит функции для получения, сортировки и фильтрации
данных о рынках из базы данных.

Использует MarketCollection для работы с данными.

TODO: Перенести функции из marketList.py:
    - get_all_markets_filtered_by_column(col, filter, user) — фильтрация по колонке
    - get_market_by_id(market_id) — получение одного рынка по ID
    - get_market_references(market_id) — получение связей рынка
    - prepare_ordered_list(markets) — переиндексация для пагинации
"""
from DAL.datalib2 import get_market
from UI.column_helper import COLUMNS_INFO
from models.collections.market_collection import MarketCollection
from models.entities.market import Market


def get_markets_ordered_by_mode(mode):
    """Получает все рынки с резолвингом локаций и упорядочиванием.

    Загружает рынки из БД, переключает режим локаций (ID → названия)
    и формирует словарь с ключами 'num' (порядковый номер) или 'uid' (ID рынка).

    Args:
        mode: Режим ключевания — 'num' или 'uid'

    Returns:
        dict: Словарь {ключ: Market}
    """
    market_base = MarketCollection.from_db()
    market_base.change_mode()
    num  = 1
    ordered_market_base = {}
    for market_id, market_info in market_base.market_dict.items():
        match mode:
            case 'num':
                ordered_market_base.update({num: market_info})
            case 'uid':
                ordered_market_base.update({market_id: market_info})
        num += 1
    return ordered_market_base


def get_all_markets_ordered_by_column(column_number, order=False, user=None):
    """Получает данные о всех рынках, отсортированные по указанной колонке.

    Args:
        column_number (int): Номер колонки для сортировки (1-9)
        order: Сортировка — 'a' (по возрастанию), 'd' (по убыванию)
        user: Словарь пользователя (для колонки distance)

    Returns:
        tuple: (dict_рынков, column_info) или None (в процессе разработки)
    """
    column = COLUMNS_INFO[column_number]
    match order:
        case 'a':
            order = False
        case 'd':
            order = True
    market_base = get_markets_ordered_by_mode('num')
    for m in market_base.keys():
        dict_market = market_base[m].get_as_dict()
        dict_market.update({'number' : m})
        market_base[m]  = dict_market
    if column['name'] == 'distance':
        pass
        #market_base =  geoLib.get_distance(user, market_base)
    sorting_base = {}
    for market_id, market_info in market_base.items():
        sorting_base.update({market_id: market_info[column['name']]})
    sorted_items = sorted(sorting_base.items(), key=lambda x: x[1], reverse=order)
    ordered_market_base = dict()
    for item_id in sorted_items:
        ordered_market_base.update({item_id[0]: market_base[item_id[0]]})
    return ordered_market_base, column
def prepare_ordered_list(markets):
    """Переиндексация dict с 1 для корректной пагинации."""
    markets_for_show = dict()
    for index, (key, value) in enumerate(markets.items(), start = 1):
        markets_for_show.update({index: value})
    return markets_for_show

def get_market_by_id(market_id):
    market = get_market(market_id)
    market = Market.get_as_dict(market)
    print('s')
