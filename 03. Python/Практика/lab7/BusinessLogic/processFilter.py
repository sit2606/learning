"""
processFilter — модуль обработки фильтрации рынков.

Содержит функцию process(), которая применяет фильтр к списку рынков
с помощью get_all_markets_ordered_by_column().

Использование:
    from BusinessLogic.processFilter import process
"""
from BusinessLogic.marketList import get_all_markets_ordered_by_column


def process(column, filter):
    """
    Обрабатывает фильтрацию рынков по колонке и значению.

    Args:
        column: номер колонки для фильтрации.
        filter: значение фильтра (строка или кортеж (знак, значение) для числовых колонок).

    Returns:
        dict: отфильтрованный словарь рынков.
    """
    market_base = get_all_markets_ordered_by_column(column)
