from model.entities.Board import Board
from model.entities.Config import Config
from model.entities.helpers.statuses import GameState, ShotState


class Game:
    def __init__(self, config: Config):
        pass

    # === Состояние игры ===
    def get_state(self) -> GameState:
        pass

    def switch_turn(self):
        pass

    def is_game_over(self) -> bool:
        pass

    # === Расстановка кораблей (SETUP) ===
    def place_ship(self, ship) -> bool:
        pass

    def can_place_ship(self, ship) -> bool:
        pass

    def start_game(self):
        pass


    def make_shot(self, x: int, y: int) -> ShotState:
        pass

    def get_winner(self) -> str:
        pass
