"""
market_queries — запросы к данным о фермерских рынках (OOP-версия).

Модуль содержит функции для получения, сортировки и фильтрации
данных о рынках из базы данных SQLite.

Функции:
    get_markets_ordered_by_mode(mode) — все рынки с резолвингом локаций
    get_all_markets_ordered_by_column(col, order, user) — сортировка по колонке
    get_market_by_id(market_id) — получение одного рынка по ID со справочниками
    get_all_markets_filtered_by_column(col, filter, user) — фильтрация по колонке
    prepare_ordered_list(markets) — переиндексация для пагинации


"""
from BusinessLogic import processFilter, geoLib
from view.helpers.column_helper import COLUMNS_INFO
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




def get_all_markets_ordered_by_column(column_number, order=False, coords=None):
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
        market_base =  geoLib.get_distance(coords, market_base)
    sorting_base = {}
    for market_id, market_info in market_base.items():
        sorting_base.update({market_id: market_info[column['name']]})
    with_values = {k: v for k, v in sorting_base.items() if v is not None}
    without_values = {k: v for k, v in sorting_base.items() if v is None}
    sorted_items = list(sorted(with_values.items(), key=lambda x: x[1], reverse=order)) + list(without_values.items())
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
    """Получает рынок по ID со всеми справочниками.

    Делегирует вызов Market.from_db() — загружает из БД,
    резолвит локации, загружает связи (banking, grocery, media).

    Args:
        market_id: ID рынка (FMID)

    Returns:
        Market: объект рынка с заполненными полями
    """
    return Market.from_db(market_id=market_id)

def get_all_markets_filtered_by_column(column, filter=None, coords=None):
    """Фильтрует и сортирует рынки по колонке с критерием.

    Получает все рынки через get_all_markets_ordered_by_column(),
    применяет фильтр через processFilter.process(),
    сортирует результат и переиндексирует для пагинации.

    Args:
        column (int): Номер колонки (1-9) из COLUMNS_INFO
        filter: Критерий фильтрации. Для текстовых — строка (подстрока).
                Для числовых — кортеж (знак_сравнения, значение_строка).
        user: Словарь пользователя (для колонки distance)

    Returns:
        tuple: (dict_рынков, column_info) — отфильтрованный словарь
               (с ключами от 1) и dict колонки {name, type}
    """
    market_list, column_info = get_all_markets_ordered_by_column(column, coords=coords)
    market_base = processFilter.process(market_list, column, filter)
    sorting_base = {}
    for market_id, market_info in market_base.items():
        sorting_base.update({market_id: market_info[column_info['name']]})
    sorted_items = sorted(sorting_base.items(), key=lambda x: x[1])
    ordered_market_base = dict()
    for item_id in sorted_items:
        ordered_market_base.update({item_id[0]: market_base[item_id[0]]})
    ordered_market_base = prepare_ordered_list(ordered_market_base)
    return ordered_market_base, column_info