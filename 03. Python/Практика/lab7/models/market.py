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
    def from_dict(self, data):
        return Market(id=data["id"], data=data)
class MarketData():
    def __init__(self):
        pass
