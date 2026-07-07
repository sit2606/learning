"""
processFilter — модуль обработки фильтрации рынков.

Содержит функцию process(), которая применяет фильтр к списку рынков
с помощью get_all_markets_ordered_by_column().

Использование:
    from BusinessLogic.processFilter import process
"""
from UI.column_helper import COLUMNS_INFO


def process(market_list, column, filter_value):
    """
    Обрабатывает фильтрацию рынков по колонке и значению.

    Args:
        column: номер колонки для фильтрации.
        filter: значение фильтра (строка или кортеж (знак, значение) для числовых колонок).

    Returns:
        dict: отфильтрованный словарь рынков.
    """
    column_to_filter = COLUMNS_INFO[column]
    filtered_market = {}
    print('s')
    if column_to_filter['type'] == 'text':
        filter_value = filter_value.lower().strip()
        for key,value in market_list.items():
            if filter_value in value[column_to_filter['name']].lower().strip():
                filtered_market.update({key : value})
        return filtered_market
    if column_to_filter['type'] == 'numeric':
            match filter_value[0]:
                    case '>':
                        for key,value in market_list.items():
                            try:
                                if float(value[column_to_filter['name']]) > float(filter_value[1]):
                                    filtered_market.update({key : value})
                            except ValueError:
                                continue
                    case '<':
                        for key,value in market_list.items():
                            try:
                                if float(value[column_to_filter['name']]) < float(filter_value[1]):
                                    filtered_market.update({key : value})
                            except ValueError:
                                continue
                    case '>=':
                        for key,value in market_list.items():
                            try:
                                if float(value[column_to_filter['name']]) >= float(filter_value[1]):
                                    filtered_market.update({key : value})
                            except ValueError:
                                continue
                    case '<=':
                        for key,value in market_list.items():
                            try:
                                if float(value[column_to_filter['name']]) <= float(filter_value[1]):
                                    filtered_market.update({key : value})
                            except ValueError:
                                continue
                    case '=':
                        for key,value in market_list.items():
                            try:
                                if float(value[column_to_filter['name']]) == float(filter_value[1]):
                                    filtered_market.update({key : value})
                            except ValueError:
                                continue
            return filtered_market


