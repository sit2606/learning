"""
Коллекция рынков (Group Entity).

Содержит класс MarketCollection для управления коллекцией рынков:
- Хранит все рынки в словаре {id: Market}
- Предоставляет factory-методы для создания из разных источников

Использование:
    >>> # Из базы данных
    >>> collection = MarketCollection.from_db()

    >>> # Из списка словарей
    >>> collection = MarketCollection.from_list(markets_data)

    >>> # Пустая коллекция
    >>> collection = MarketCollection()
"""

from DAL.datalib2 import get_all_markets
from models.entities.market import Market, Location
from models.entities.reference import Reference


class MarketCollection:
    """Коллекция фермерских рынков.

    Управляет словарём рынков {id: Market}. Предоставляет factory-методы
    для создания коллекции из разных источников (БД, список, словарь).

    Attributes:
        market_dict (dict): Словарь рынков {id: Market}

    Example:
        >>> collection = MarketCollection.from_db()
        >>> collection.market_dict[1]  # Market с id=1
    """

    def __init__(self, market_info: dict = None):
        """Инициализирует коллекцию рынков.

        Args:
            market_info (dict, optional): Словарь {id: Market}.
                                         Если не передан — создаёт пустую коллекцию.
        """
        self.market_dict = market_info if market_info is not None else {}
        if market_info:
            base_market = market_info.popitem()
            if base_market[1].location.state.isnumeric():
                self.ref_mode = 'id'
            elif base_market[1].location.state.isalpha():
                self.ref_mode = 'value'
    @classmethod
    def from_db(cls):
        """Создаёт коллекцию из базы данных.

        Загружает все рынки из таблицы MARKETS через get_all_markets().

        Returns:
            MarketCollection: коллекция с заполненными рынками
        """
        db_markets = get_all_markets()
        market_dict = {m['id']: Market.from_dict(m) for m in db_markets}
        return cls(market_info=market_dict)
    @classmethod
    def from_dict(cls, data):
        """Создаёт коллекцию из словаря {id: Market}.

        Args:
            data (dict): Словарь {id: Market}

        Returns:
            MarketCollection: коллекция, обёрнутая из переданного словаря

        Example:
            >>> markets = {1: Market(1), 2: Market(2)}
            >>> collection = MarketCollection.from_dict(markets)
        """
        return cls(market_info=data)
    @classmethod
    def from_list(cls, market_list):
        """Создаёт коллекцию из списка Market или словарей.

        Args:
            market_list: Список объектов Market или словарей с данными

        Returns:
            MarketCollection
        """
        return cls({m['id']: Market.from_dict(m) for m in market_list})
    def change_mode(self):
        """Переключает режим отображения локаций для всех рынков в коллекции.

        - 'id' → 'value': заменяет числовые ID на названия из справочников
        - 'value' → 'id': заменяет названия на числовые ID

        Делегирует вызов Market.change_mode() для каждого рынка в коллекции.
        """
        match self.ref_mode:
            case 'id':
                city_ref = Reference('CITY').get_all_with_keys()
                county_ref = Reference('COUNTY').get_all_with_keys()
                state_ref = Reference('STATE').get_all_with_keys()
                street_ref = Reference('STREET').get_all_with_keys()
                zip_ref = Reference('ZIP').get_all_with_keys()
                for market in self.market_dict.values():
                    market.location.city = city_ref[int(market.location.city)]
                    market.location.county = county_ref[int(market.location.county)]
                    market.location.state = state_ref[int(market.location.state)]
                    market.location.street = street_ref[int(market.location.street)]
                    market.location.zip = zip_ref[int(market.location.zip)]
                self.ref_mode = 'value'
            case 'value':
                city_ref = Reference('CITY').get_all_with_names()
                county_ref = Reference('COUNTY').get_all_with_names()
                state_ref = Reference('STATE').get_all_with_names()
                street_ref = Reference('STREET').get_all_with_names()
                zip_ref = Reference('ZIP').get_all_with_names()
                for market in self.market_dict.values():
                    market.location.city = city_ref[market.location.city]
                    market.location.county = county_ref[market.location.county]
                    market.location.state = state_ref[market.location.state]
                    market.location.street = street_ref[market.location.street]
                    market.location.zip = zip_ref[market.location.zip]
                self.ref_mode = 'id'
    def as_list(self):
        """Конвертирует коллекцию в список Market.

        Returns:
            list[Market]: Список всех рынков в коллекции
        """
        return [m for m in self.market_dict.values()]

    def as_dict(self):
        pass