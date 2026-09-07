from enum import Enum


class CellState(Enum):
    FILL = 'Fill'
    EMPTY = 'Empty'
    HIT = 'Hit'
    MISS = 'Miss'
class ShipState(Enum):
    FULL = 'Full'
    WOUNDED = 'Wounded'
    KILLED = 'Killed'

class GameState(Enum):
    SETUP = 'Setup'
    PLAYER_TURN = 'PlayerTurn'
    COMPUTER_TURN = 'ComputerTurn'
    GAME_OVER = 'GameOver'