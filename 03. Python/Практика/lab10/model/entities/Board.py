from model.entities.Ship import Ship
from model.entities.Config import Config
from model.entities.helpers.statuses import ShotState


class Board:
    def __init__(self, settings: Config):
        pass
    def place_ship(self, ship: Ship):
        pass
    def validate_ship_position(self, ship: Ship):
        pass
    def shot(self, x,y) -> ShotState:
        pass
    def get_ships_state(self):
        pass