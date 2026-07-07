"""
marketList — бизнес-логика для работы со списком рынков.

Модуль предоставляет функции для получения и сортировки данных
о фермерских рынках из MARKET_INFO.csv:

- get_all_markets(mode): все рынки с резолвингом ID → имена ('uid' или 'num')
- get_all_markets_ordered_by_column(col, order): сортировка по колонке
- get_all_markets_filtered_by_column(col, filter): фильтрация по колонке с критерием
- prepare_ordered_list(markets): переиндексация для пагинации
- get_market_by_id(market_id): получение одного рынка по Id
- get_market_references(market_id): получение связей рынка со справочниками
- update_market_info(market_info): обновление данных рынка

Зависимости:
- BusinessLogic.processFilter: обработка фильтрации
- DAL.dataLib: обновление данных рынка
- DAL.fileLib: чтение MARKET_INFO.csv
- DAL.referenceLib: чтение справочников и связей
- UI.column_helper: COLUMNS_INFO (тип и имя колонок)

Использование:
    from BusinessLogic.marketList import get_all_markets, get_market_by_id
"""
from BusinessLogic import processFilter
from DAL.dataLib import update_market
from DAL.fileLib import get_raw_markets_from_file
from DAL.referenceLib import get_reference_with_uid_as_key, get_all_connections_by_market_id, \
    get_reference_with_name_as_key
from UI.column_helper import COLUMNS_INFO


def get_market_references(market_id):
    """
    Получает все связи рынка со справочниками (банки, товары, соцсети).

    Args:
        market_id: Идентификатор рынка.

    Returns:
        tuple: (market_x_banking_info, market_x_grocery, market_x_social_media) —
               три словаря со связями рынка.
    """
    _market_id = market_id
    market_x_banking_info = get_all_connections_by_market_id('MarketXBankingInfo', _market_id)
    market_x_grocery = get_all_connections_by_market_id('MarketXGrocery', _market_id)
    market_x_social_media = get_all_connections_by_market_id('MarketXSocialMedia', _market_id)
    return market_x_banking_info,market_x_grocery,market_x_social_media
def get_all_markets(mode):
    """
    Получает данные о всех фермерских рынках с порядковой нумерацией.

    Читает MARKET_INFO.csv, резолвит ID городов/округов/штатов в имена,
    добавляет порядковый номер и market_id.

    Args:
        mode: Режим ключевания словаря:
            'num' — ключ порядковый номер (для пагинации),
            'uid' — ключ market_id.

    Returns:
        dict: словарь {ключ: {атрибуты_рынка, number, market_id}}.
    """
    market_base = get_raw_markets_from_file()
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
        match mode:
            case 'num':
                ordered_market_base.update({num: market_info})
            case 'uid':
                ordered_market_base.update({market_id: market_info})
        num += 1
    return ordered_market_base
def get_all_markets_ordered_by_column(column_number, order = False):
    """
    Получает данные о всех фермерских рынках, отсортированные по указанной колонке.

    Использует COLUMNS_INFO для маппинга номера колонки на имя и тип.
    Поддерживаемые колонки: 1-номер, 2-ID, 3-город, 4-графство,
    5-штат, 6-название, 7-индекс, 8-ср. оценка.

    Args:
        column_number (int): номер колонки для сортировки (1-8).
        order (str): 'a' — по возрастанию, 'd' — по убыванию.

    Returns:
        tuple: (dict_рынков, column_info) — отсортированный словарь и dict колонки
               {name: имя_колонки, type: тип_колонки}.
    """
    column = COLUMNS_INFO[column_number]
    match order:
        case 'a':
            order = False
        case 'd':
            order = True
    market_base = get_all_markets('num')
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
    """
    Получает подробные данные одного рынка по Id.

    Формирует структуру:
    {
        'basic_info': {market_id, marketname, street, city, county, state, zip, season*},
        'media_info': {имя_соцсети: url, ...},
        'bank_info': {способ_оплаты: да/нет, ...},
        'grocery_info': {тип_товара: да/нет, ...}
    }

    Args:
        market_id: Идентификатор рынка.

    Returns:
        dict: структура с данными рынка или None если не найден.
    """
    market_base = get_all_markets('uid')
    _market_id = market_id
    try:
        market_info = {market_id: market_base[str(_market_id)]}
        market_x_banking_info, market_x_grocery , market_x_social_media  = get_market_references(_market_id)
        banking_reference = get_reference_with_uid_as_key("BANKING_INFO", "Common")
        grocery_reference = get_reference_with_uid_as_key("GROCERY_TYPES", "Common")
        media_reference = get_reference_with_uid_as_key("MEDIA", "Common")
        bank_info = {}
        grocery_info = {}
        media_info = {}
        market_info.update({'basic_info': market_info[_market_id]})
        for item in market_x_social_media[str(_market_id)]:
            name = media_reference[str(item)]
            status = market_x_social_media[str(_market_id)][str(item)]
            media_info.update({name: status})
        market_info.update({'media_info': media_info})
        for item in market_x_banking_info[str(_market_id)]:
            name = banking_reference[str(item)]
            status = market_x_banking_info[str(_market_id)][str(item)]
            bank_info.update({name: status})
        market_info.update({'bank_info': bank_info})
        for item in market_x_grocery[str(_market_id)]:
            name = grocery_reference[str(item)]
            status = market_x_grocery[str(_market_id)][str(item)]
            grocery_info.update({name: status})
        market_info.update({'grocery_info': grocery_info})
        market_info.pop(_market_id)
        return market_info
    except KeyError:
        return None

def update_market_info(market_info):
    """
    Обновляет данные рынка в MARKET_INFO.csv.

    Конвертирует имена городов/округов/штатов обратно в UUID
    и вызывает update_market() из dataLib.

    Args:
        market_info (dict): Словарь с данными рынка, содержащий
            'basic_info' с полями market_id, city, county, state и др.
    """
    _market_id = market_info['basic_info']['market_id']
    for key, value in market_info['basic_info'].items():
        if key == 'city':
            city_uid = get_reference_with_name_as_key("CITY", 'Common')
            market_info['basic_info'].update({"city": city_uid[value]})
        if key == 'county':
            county_uid = get_reference_with_name_as_key("COUNTY", 'Common')
            market_info['basic_info'].update({"county": county_uid[value]})
        if key == 'state':
            state_uid = get_reference_with_name_as_key("STATE", 'Common')
            market_info['basic_info'].update({"state": state_uid[value]})
    market_info['basic_info'].pop('number')
    update_market(market_info['basic_info'])

def get_all_markets_filtered_by_column(column, filter = None):
    """
    Фильтрует и сортирует рынки по указанной колонке и критерию.

    Использует processFilter() для первичной обработки,
    затем сортирует результат по алфавиту/порядку.

    Args:
        column: dict колонки {name: имя, type: тип} из COLUMNS_INFO.
        filter: критерий фильтрации (строка для текстовых или
                кортеж (знак, значение) для числовых колонок).

    Returns:
        tuple: (dict_рынков, column_info) — отфильтрованный словарь и dict колонки.
    """

    market_list, column_info = get_all_markets_ordered_by_column(column)
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