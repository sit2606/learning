"""
Модель данных для фермерского рынка.

Содержит dataclass-ы для группировки информации о рынке:
- Marketinfo: основная информация (название, оценка, расстояние)
- Timesheet: расписание по сезонам
- Coordinates: географические координаты
- Location: местоположение (город, округ, штат, индекс, улица)
- Market: основной класс, объединяющий все группы
"""

from dataclasses import dataclass


@dataclass
class Marketinfo:
    """Основная информация о рынке."""
    marketname: str = None
    score: float = None
    distance: float = None


@dataclass
class Timesheet:
    """Расписание работы по сезонам."""
    season1date: str = None
    season1time: str = None
    season2date: str = None
    season2time: str = None
    season3date: str = None
    season3time: str = None
    season4date: str = None
    season4time: str = None


@dataclass
class Coordinates:
    """Географические координаты рынка."""
    latitude: float = None
    longitude: float = None


@dataclass
class Location:
    """Местоположение рынка."""
    zip: str = None
    street: str = None
    city: str = None
    state: str = None
    county: str = None


class Market:
    """Класс фермерского рынка.

    Объединяет информацию из всех групп: Marketinfo, Timesheet,
    Coordinates, Location.

    Attributes:
        id: Уникальный идентификатор рынка (FMID)
        market_info: Основная информация
        timesheet: Расписание
        coordinates: Координаты
        location: Местоположение

    Example:
        >>> market = Market("12345")
        >>> market.market_info.marketname = "Farmers Market"
    """
    def __init__(self, id, data = None):
        """Инициализирует рынок с указанным id.

        Args:
            id: Уникальный идентификатор рынка
        """
        self.id = id
        self.market_info = Marketinfo()
        self.timesheet = Timesheet()
        self.coordinates = Coordinates()
        self.location = Location()
        if data is not None:
            self.timesheet = Timesheet(**data)
            self.coordinates = Coordinates(**data)
            self.market_info=Marketinfo(**data)
            self.location=Location(**data)
    def __str__(self):
        """Возвращает строковое представление (id рынка)."""
        return str(self.id)
    @classmethod
    #TODO ПРОВЕРИТЬ КАК ЭТО РАБОТАЕТ
    def from_dict(cls, data):
        market_info = {
            'marketname': data.get('marketname'),
            'score': data.get('score'),
            'distance': None  # расчётное поле, не в БД
        }
        timesheet = {
            'season1date': data.get('season1date'),
            'season1time': data.get('season1time'),
            'season2date': data.get('season2date'),
            'season2time': data.get('season2time'),
            'season3date': data.get('season3date'),
            'season3time': data.get('season3time'),
            'season4date': data.get('season4date'),
            'season4time': data.get('season4time'),
        }
        coordinates = {
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
        }
        location = {
            'city': data.get('city'),
            'county': data.get('county'),
            'state': data.get('state'),
            'zip': data.get('zip'),
            'street': data.get('street'),
        }

        market = cls(id=data['id'])
        market.market_info = Marketinfo(**market_info)
        market.timesheet = Timesheet(**timesheet)
        market.coordinates = Coordinates(**coordinates)
        market.location = Location(**location)
        return market
class MarketData:
    def __init__(self, market_info):
        self.market_list = {}
        for market in market_info:
            self.market_list.update({market['id']: Market.from_dict(market)})
