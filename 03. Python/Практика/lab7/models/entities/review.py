from datetime import datetime

from DAL.reviewlib2 import create_review
from models.entities.market import Market
from models.entities.user import User


class Review:
    def __init__(self,user : User , market: Market,  id=None, review_date=None ):
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
        self.review_text = text
    def set_score(self, score):
        self.score = score
    def save_to_db(self):
        info = {}
        info['user_id'] = self.user_id
        info['market_id'] = self.market_id
        info['review_date'] = self.review_date
        info['review_text'] = self.review_text
        info['score'] = self.score
        create_review(info)
    @classmethod
    def from_dict(cls, data):
        rev = cls(user=User.from_db(data['user_id']), market=Market.from_db(market_id=data['market_id']), id=data['id'], review_date=data['review_date'])
        rev.set_text(data['review_text'])
        rev.set_score(data['score'])
        return rev
    def get_as_dict(self):
        return {
            'id': self.id,
            'market_id': self.market_id,
            'review_date': self.review_date,
            'review_text': self.review_text,
            'score': self.score,
            'text': self.review_text
        }