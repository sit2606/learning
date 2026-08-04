from datetime import datetime

from DAL.reviewlib2 import create_review
from models.entities.market import Market
from models.entities.user import User


class Review:
    def __init__(self,user : User , market: Market,  id=None  ):
        self.id = id
        self.review_date = str(datetime.now())
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
