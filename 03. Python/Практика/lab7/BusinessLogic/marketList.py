"""
marketList — бизнес-логика для работы со списком рынков.

Модуль предоставляет функцию get_all_markets() для получения
данных о фермерских рынках из CSV-файла MARKET_INFO.csv.

Использование:
    from BusinessLogic.marketList import get_all_markets
"""

from DAL.fileLib import get_markets_base
from DAL.referenceLib import get_reference


def get_all_markets():
    """
    Получает данные о всех фермерских рынках.

    Вызывает fileLib.get_markets_base() для чтения MARKET_INFO.csv.

    Returns:
        csv.DictReader: объект чтения CSV с данными о рынках.
    """
    market_base = get_markets_base()
    get_reference('CITY',)
    return




