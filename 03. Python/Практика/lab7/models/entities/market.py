"""
Базовые сущности рынка.

Содержит dataclass-ы для группировки информации о рынке:
- Marketinfo: основная информация (название, оценка, расстояние)
- Timesheet: расписание по сезонам
- Coordinates: географические координаты
- Location: местоположение (город, округ, штат, индекс, улица)
- Market: основной класс, объединяющий все группы

Иерархия:
    Market
    ├── market_info: Marketinfo
    ├── timesheet: Timesheet
    ├── coordinates: Coordinates
    └── location: Location
"""

from dataclasses import dataclass

from models.entities.reference import Reference


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
        market_info: Основная информация (Marketinfo)
        timesheet: Расписание (Timesheet)
        coordinates: Координаты (Coordinates)
        location: Местоположение (Location)

    Example:
        >>> market = Market("12345")
        >>> market.market_info.marketname = "Farmers Market"

        >>> data = {"id": 1, "marketname": "Рынок", "city": "Москва"}
        >>> market = Market.from_dict(data)
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
        if self.location.state is not None:
            if self.location.state.isnumeric():
                self.ref_mode = 'id'
            elif self.location.city.isalpha():
                self.ref_mode = 'value'
    def __str__(self):
        """Возвращает строковое представление (id рынка)."""
        return str(self.id)
    @classmethod
    def from_dict(cls, data):
        """Создаёт Market из словаря/Row с данными из БД.

        Разделяет данные по группам (market_info, timesheet, coordinates, location)
        и создаёт соответствующие dataclass-ы.

        Args:
            data: dict или sqlite3.Row с ключами из таблицы MARKETS

        Returns:
            Market: объект с заполненными полями
        """
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
    def get_as_dict(self):
        """Конвертирует все поля рынка в плоский словарь.

        Объединяет поля из Marketinfo, Timesheet, Coordinates, Location
        в один словарь.

        Returns:
            dict: Словарь {имя_поля: значение}
        """
        info = {}
        for fields in self.market_info, self.timesheet, self.coordinates, self.location:
            for values in fields.__dict__:
                info.update({values: getattr(fields, values)})
        return info

    def change_mode(self):
        """Переключает режим отображения локаций (ID ↔ названия).

        - 'id' → 'value': заменяет числовые ID на названия из справочников
        - 'value' → 'id': заменяет названия на числовые ID

        Использует справочники CITY, COUNTY, STATE, STREET, ZIP.
        """
        match self.ref_mode:
            case 'id':
                city_ref = Reference('CITY').get_all_with_keys()
                county_ref = Reference('COUNTY').get_all_with_keys()
                state_ref = Reference('STATE').get_all_with_keys()
                street_ref = Reference('STREET').get_all_with_keys()
                zip_ref = Reference('ZIP').get_all_with_keys()
                self.location.city = city_ref[int(self.location.city)]
                self.location.county = county_ref[int(self.location.county)]
                self.location.state = state_ref[int(self.location.state)]
                self.location.street = street_ref[int(self.location.street)]
                self.location.zip = zip_ref[int(self.location.zip)]
                self.ref_mode = 'value'
            case 'value':
                city_ref = Reference('CITY').get_all_with_names()
                county_ref = Reference('COUNTY').get_all_with_names()
                state_ref = Reference('STATE').get_all_with_names()
                street_ref = Reference('STREET').get_all_with_names()
                zip_ref = Reference('ZIP').get_all_with_names()
                self.location.city = city_ref[self.location.city]
                self.location.county = county_ref[self.location.county]
                self.location.state = state_ref[self.location.state]
                self.location.street = street_ref[self.location.street]
                self.location.zip = zip_ref[self.location.zip]
                self.ref_mode = 'id'