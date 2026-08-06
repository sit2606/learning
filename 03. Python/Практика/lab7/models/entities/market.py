"""
Базовые сущности рынка.

Содержит dataclass-ы для группировки информации о рынке:
- Marketinfo: основная информация (название, оценка, расстояние)
- Timesheet: расписание по сезонам
- Coordinates: географические координаты
- Location: местоположение (город, округ, штат, индекс, улица)
- BankInfo: банковские реквизиты (справочник)
- MediaInfo: соцсети (справочник)
- GroceryInfo: типы товаров (справочник)
- Market: основной класс, объединяющий все группы

Иерархия:
    Market
    ├── market_info: Marketinfo
    ├── timesheet: Timesheet
    ├── coordinates: Coordinates
    ├── location: Location
    ├── banking_info: BankInfo
    ├── media_info: MediaInfo
    └── grocery_info: GroceryInfo

Factory-методы:
    Market.from_dict(data) — из словаря/Row
    Market.from_db(market_id) — из БД с резолвингом справочников

Методы:
    get_as_dict() — конвертация в плоский словарь
    change_mode() — переключение ID ↔ названия локаций
    update() — сохранение в БД
    calculate_score() — пересчёт средней оценки из отзывов
    get_reviews() — получение всех отзывов рынка
    delete() — удаление рынка из БД
"""

from dataclasses import dataclass


from DAL.referencelib2 import  get_all_connections_by_market_id
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
@dataclass
class BankInfo:
    banking : dict = None
    ref_mode :str = 'id'
    def change_mode(self):
        match self.ref_mode:
            case 'id':
                bank_ref = Reference('BANKING_INFO').get_all_with_keys()
                new_banking = dict()
                for key, value in self.banking.items():
                    new_banking.update({
                        bank_ref.get(key) : value
                    })
                self.banking = new_banking
                self.ref_mode = 'value'
            case 'value':
                bank_ref = Reference('BANKING_INFO').get_all_with_names()
                new_banking = dict()
                for key, value in self.banking.items():
                    new_banking.update({
                        bank_ref.get(key) : value
                    })
                self.banking = new_banking
                self.ref_mode = 'id'
@dataclass
class MediaInfo:
    media : dict = None
    ref_mode: str = 'id'
    def change_mode(self):
        match self.ref_mode:
            case 'id':
                media_ref = Reference('MEDIA').get_all_with_keys()
                new_media = dict()
                for key, value in self.media.items():
                    new_media.update({
                        media_ref.get(key) : value
                    })
                self.media = new_media
                self.ref_mode = 'value'
            case 'value':
                media_ref = Reference('MEDIA').get_all_with_names()
                new_media = dict()
                for key, value in self.media.items():
                    new_media.update({
                        media_ref.get(key) : value
                    })
                self.media = new_media
                self.ref_mode = 'id'
@dataclass
class GroceryInfo:
    grocery : dict = None
    ref_mode: str = 'id'

    def change_mode(self):
        match self.ref_mode:
            case 'id':
                grocery_ref = Reference('GROCERY_TYPES').get_all_with_keys()
                new_grocery = dict()
                for key, value in self.grocery.items():
                    new_grocery.update({
                        grocery_ref.get(key): value
                    })
                self.grocery = new_grocery
                self.ref_mode = 'value'
            case 'value':
                grocery_ref = Reference('GROCERY_TYPES').get_all_with_names()
                new_grocery = dict()
                for key, value in self.grocery.items():
                    new_grocery.update({
                        grocery_ref.get(key): value
                    })
                self.grocery = new_grocery
                self.ref_mode = 'id'
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
        self.ref_mode = 'id'
        self.market_info = Marketinfo()
        self.timesheet = Timesheet()
        self.coordinates = Coordinates()
        self.location = Location()
        self.banking_info = BankInfo()
        self.media_info = MediaInfo()
        self.grocery_info = GroceryInfo()
        if data is not None:
            self.timesheet = Timesheet(**data)
            self.coordinates = Coordinates(**data)
            self.market_info=Marketinfo(**data)
            self.location=Location(**data)
            self.banking_info=BankInfo(**data)
            self.media_info=MediaInfo(**data)
            self.grocery_info=GroceryInfo(**data)
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
        media = data.get('media_info')
        if media is not None:
            media_info = {k:v for k, v in media.items()}
        else:
            media_info = dict()
        grocery = data.get('grocery_info')
        if grocery is not None:
            grocery_info = {k:v for k, v in grocery.items()}
        else:
            grocery_info = dict()
        banking = data.get('banking_info')
        if banking is not None:
            banking_info = {k:v for k, v in banking.items()}
        else:
            banking_info = dict()
        market = cls(id=data['id'])
        market.market_info = Marketinfo(**market_info)
        market.timesheet = Timesheet(**timesheet)
        market.coordinates = Coordinates(**coordinates)
        market.location = Location(**location)
        market.media_info = MediaInfo(**media_info)
        market.grocery_info = GroceryInfo(**grocery_info)
        market.banking_info = BankInfo(**banking_info)
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
        info.update({'market_id': self.id})
        return info
    def get_ui_dict(self):
        """Конвертирует все поля рынка в плоский словарь.

        Объединяет поля из Marketinfo, Timesheet, Coordinates, Location
        в один словарь.

        Returns:
            dict: Словарь {имя_поля: значение}
        """
        basic_info = {}
        info = {}
        for fields in self.market_info, self.timesheet, self.coordinates, self.location:
            for values in fields.__dict__:
                basic_info.update({values: getattr(fields, values)})
        basic_info.update({'market_id': str(self.id)})
        info.update({'basic_info': basic_info})
        if self.banking_info is not None:
            info.update({'bank_info': self.banking_info.banking})
        if self.grocery_info is not None:
            info.update({'grocery_info': self.grocery_info.grocery})
        if self.media_info is not None:
            info.update({'media_info': self.media_info.media})

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
                self.banking_info.change_mode()
                self.media_info.change_mode()
                self.grocery_info.change_mode()
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
                self.banking_info.change_mode()
                self.media_info.change_mode()
                self.grocery_info.change_mode()
                self.ref_mode = 'id'

    @classmethod
    def from_db(cls, market_id):
        """Загружает рынок по ID из БД с резолвингом справочников.

        Создаёт Market через get_market(), переключает локации на названия (change_mode),
        загружает связи из таблиц MarketXBankingInfo, MarketXGrocery, MarketXSocialMedia.

        Args:
            market_id: ID рынка (FMID)

        Returns:
            Market: объект с заполненными полями и справочниками

        Example:
            >>> market = Market.from_db(1018261)
            >>> market.location.city  # "Santa Fe" вместо "42"
        """
        from DAL.datalib2 import get_market
        market = get_market(market_id)
        if market is None:
            return None
        banking = get_all_connections_by_market_id("MarketXBankingInfo", market_id=market_id)
        grocery = get_all_connections_by_market_id("MarketXGrocery", market_id=market_id)
        media = get_all_connections_by_market_id("MarketXSocialMedia", market_id=market_id)
        market.banking_info = BankInfo(banking)
        market.grocery_info = GroceryInfo(grocery)
        market.media_info = MediaInfo(media)
        market.change_mode()
        return market

    def update(self):

        """Сохраняет изменения рынка в БД.

        Делегирует вызов DAL.datalib2.update_market(). Если ref_mode = 'value',
        автоматически конвертирует названия обратно в ID перед записью.
        """
        from DAL.datalib2 import update_market
        update_market(self)
    def calculate_score(self):
        """Пересчитывает среднюю оценку рынка на основе отзывов.

        Загружает все отзывы, вычисляет среднее, обновляет score и сохраняет в БД.
        """
        from DAL.reviewlib2 import get_review_by_market_id
        from statistics import mean
        reviews = get_review_by_market_id(self.id)
        score = []
        for review in reviews:
            score.append(float(review.score))
        score = mean(score)
        self.market_info.score = score
        self.update()
    def get_reviews(self):
        """Возвращает все отзывы для данного рынка.

        Returns:
            list[Review]: Список объектов Review
        """
        from DAL.reviewlib2 import get_review_by_market_id
        return get_review_by_market_id(self.id)
    def delete(self):
        """Удаляет рынок из таблицы MARKETS."""
        from DAL.datalib2 import delete_market
        return delete_market(self.id)