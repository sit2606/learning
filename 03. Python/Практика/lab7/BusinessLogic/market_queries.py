"""
market_queries — запросы к данным о фермерских рынках.

Модуль содержит функции для получения, сортировки и фильтрации
данных о рынках из базы данных.

TODO: Перенести функции из marketList.py:
    - get_all_markets_ordered_by_column(col, order, user) — сортировка по колонке
    - get_all_markets_filtered_by_column(col, filter, user) — фильтрация по колонке
    - get_market_by_id(market_id) — получение одного рынка по ID
    - get_market_references(market_id) — получение связей рынка
    - prepare_ordered_list(markets) — переиндексация для пагинации
"""
from UI.column_helper import COLUMNS_INFO
from models.collections.market_collection import MarketCollection


def get_markets_ordered_by_mode(mode):
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
def get_all_markets_ordered_by_column(column_number, order = False, user = None):
    column = COLUMNS_INFO[column_number]
    match order:
        case 'a':
            order = False
        case 'd':
            order = True
    market_base = get_markets_ordered_by_mode('num')
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