"""
AppController — центральный контроллер приложения.

Хранит состояние сессии (self.user) и предоставляет
методы-кейсы для View (консоль и PyQt).

Зависимости:
- BusinessLogic.market_queries: запросы к рынкам
- BusinessLogic.geoLib: гео-расчёты
- models.entities.*: сущности User, Market, Review, Reference
- DAL.*: userlib2, reviewlib2, referencelib2
"""

import bcrypt

from BusinessLogic import geoLib
from BusinessLogic.market_queries import (
    get_markets_ordered_by_mode,
    get_all_markets_ordered_by_column,
    prepare_ordered_list,
    get_market_by_id,
    get_all_markets_filtered_by_column,
)
from DAL import referencelib2, reviewlib2, userlib2
from models.entities.reference import Reference
from models.entities.review import Review
from models.entities.user import User


class AppController:
    def __init__(self):
        self.user = None

    # ── Инициализация БД ──────────────────────────────────

    def init_db(self):
        """Создаёт таблицы и импортирует CSV."""
        from DAL import requiredFiles, filelib2, datalib2
        requiredFiles.prepare_refs()
        requiredFiles.create_market_table()
        requiredFiles.create_review_table()
        requiredFiles.create_user_table()
        datalib2.add_many(filelib2.read_csv())

    # ── Рынки: получение ──────────────────────────────────

    def get_all_markets(self) -> dict | None:
        """Все рынки с нумерацией."""
        markets = get_markets_ordered_by_mode('num')
        if markets is None:
            return None
        for k, v in markets.items():
            markets[k] = v.get_as_dict()
        return markets

    def get_market_by_id(self, market_id: int) -> dict | None:
        """Подробная информация об одном рынке."""
        market = get_market_by_id(market_id)
        if market is None:
            return None
        return market

    def get_ordered_markets(self, column: int, order: str) -> tuple:
        """Рынки, отсортированные по колонке."""
        markets, column_info = get_all_markets_ordered_by_column(column, order)
        markets = prepare_ordered_list(markets)
        return markets, column_info

    def get_filtered_markets(self, column: int, filter_value, coords: dict = None) -> tuple:
        """Рынки, отфильтрованные по критерию."""
        if coords is None and self.user is not None:
            coords = {'latitude': self.user.latitude, 'longitude': self.user.longitude}
        return get_all_markets_filtered_by_column(column, filter_value, coords)

    def get_market_reviews(self, market_id: int) -> list:
        """Отзывы для рынка с именами авторов."""
        market = get_market_by_id(market_id)
        if market is None:
            return []
        reviews = market.get_reviews()
        result = []
        for review in reviews:
            author = User.from_db(review.user_id)
            rev = review.get_as_dict()
            rev['user_name'] = f"{author.firstname} {author.lastname}"
            result.append(rev)
        return result, market.market_info.score

    def delete_market(self, market_id: int) -> bool:
        """Удаляет рынок и все его связи."""
        referencelib2.delete_all_connections_by_market_id(market_id, 'MarketXBankingInfo')
        referencelib2.delete_all_connections_by_market_id(market_id, 'MarketXGrocery')
        referencelib2.delete_all_connections_by_market_id(market_id, 'MarketXSocialMedia')
        reviewlib2.delete_reviews_by_market_id(market_id)
        market = get_market_by_id(market_id)
        if market:
            market.delete()
            return True
        return False

    # ── Рынки: поиск по ZIP ───────────────────────────────

    def search_by_zip(self, postalcode: str, radius: float) -> tuple | None:
        """Рынки в радиусе от почтового индекса."""
        ref = Reference("ZIP")
        if ref.get_entry(entry_name=postalcode) is None:
            return None
        coords = {}
        coords['latitude'], coords['longitude'] = geoLib.get_zip_coords(postalcode)
        return get_all_markets_filtered_by_column(9, ('<', radius), coords)

    # ── Пользователи: регистрация / авторизация ───────────

    def register(self, username: str, password: str,
                 firstname: str, lastname: str,
                 latitude: str = '', longitude: str = '') -> User | None:
        """Регистрирует пользователя. Возвращает User или None."""
        existing = User.from_db(username=username)
        if existing.username == username:
            return None  # логин занят

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
        user = User()
        user.username = username
        user.password = hashed.decode('utf-8')
        user.firstname = firstname
        user.lastname = lastname
        user.latitude = latitude
        user.longitude = longitude
        user.add_to_db()
        self.user = user
        return user

    def login(self, username: str, password: str) -> User | None:
        """Авторизация. Возвращает User или None."""
        if self.user is not None:
            return self.user  # уже авторизован

        user_in_base = User.from_db(username=username)
        if user_in_base.username != username:
            return None  # пользователь не найден

        is_valid = bcrypt.checkpw(
            password.encode('utf-8'),
            user_in_base.password.encode('utf-8')
        )
        if is_valid:
            self.user = user_in_base
            return user_in_base
        return None  # неверный пароль

    def logout(self) -> None:
        """Выход из системы."""
        self.user = None

    # ── Пользователи: обновление ──────────────────────────

    def update_user(self, **fields) -> User:
        """Обновляет поля текущего пользователя."""
        for key, value in fields.items():
            setattr(self.user, key, value)
        userlib2.update_user(self.user)
        return self.user

    def is_logged_in(self) -> bool:
        """Проверяет авторизацию."""
        return self.user is not None

    # ── Отзывы ────────────────────────────────────────────

    def add_review(self, market_id: int, score: int, text: str = '') -> bool:
        """Добавляет отзыв. Требует авторизации."""
        if self.user is None:
            return False
        market = get_market_by_id(market_id)
        if market is None:
            return False
        review = Review(self.user, market)
        review.set_score(score)
        review.set_text(text)
        review.save_to_db()
        market.calculate_score()
        return True
