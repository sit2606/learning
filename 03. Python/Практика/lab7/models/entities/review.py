"""Сущность отзыва (Review).

Содержит класс Review для создания и сохранения отзывов о рынках.

Использование:
    >>> user = User.from_db(username='test')
    >>> market = Market.from_db(1018261)
    >>> review = Review(user, market)
    >>> review.set_score(5)
    >>> review.set_text('Отличный рынок!')
    >>> review.save_to_db()
"""

from datetime import datetime

from DAL.reviewlib2 import create_review
from models.entities.market import Market
from models.entities.user import User


class Review:
    """Отзыв пользователя о фермерском рынке.

    Attributes:
        id: Идентификатор отзыва (None при создании)
        review_date: Дата и время создания (автоматически)
        user_id: ID автора отзыва
        market_id: ID рынка
        review_text: Текст отзыва
        score: Оценка (1-5)
    """

    def __init__(self,user : User , market: Market,  id=None, review_date=None ):
        """Инициализирует отзыв.

        Args:
            user (User): Автор отзыва
            market (Market): Рынок
            id: Идентификатор (None при создании)
            review_date: Дата отзыва (None = текущее время)
        """
        self.id = id
        if review_date is None:
            self.review_date = str(datetime.now())
        else:
            self.review_date = review_date
        self.user_id = user.id
        self.market_id = market.id
        self.review_text = ''
        self.score = None
    def set_text(self, text):
        """Устанавливает текст отзыва.

        Args:
            text (str): Текст отзыва
        """
        self.review_text = text
    def set_score(self, score):
        """Устанавливает оценку.

        Args:
            score (int): Оценка от 1 до 5
        """
        self.score = score
    def save_to_db(self):
        """Сохраняет отзыв в таблицу REVIEWS."""
        info = {}
        info['user_id'] = self.user_id
        info['market_id'] = self.market_id
        info['review_date'] = self.review_date
        info['review_text'] = self.review_text
        info['score'] = self.score
        create_review(info)
    @classmethod
    def from_dict(cls, data):
        """Создаёт Review из словаря (данные из БД).

        Args:
            data (dict): Словарь с ключами id, user_id, market_id,
                review_date, review_text, score

        Returns:
            Review: объект отзыва
        """
        rev = cls(user=User.from_db(user_id= data['user_id']), market=Market.from_db(market_id=data['market_id']), id=data['id'], review_date=data['review_date'])
        rev.set_text(data['review_text'])
        rev.set_score(data['score'])
        return rev
    def get_as_dict(self):
        """Конвертирует отзыв в словарь.

        Returns:
            dict: Словарь с полями id, market_id, review_date,
                review_text, score, text
        """
        return {
            'id': self.id,
            'market_id': self.market_id,
            'review_date': self.review_date,
            'review_text': self.review_text,
            'score': self.score,
            'text': self.review_text
        }
