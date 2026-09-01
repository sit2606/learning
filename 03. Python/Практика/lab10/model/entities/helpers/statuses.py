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
class ShotState(Enum):
    MISS = 'Miss'
    HIT = 'Hit'
    SUNK = 'Sunk'

class GameState(Enum):
    SETUP = 'Setup'
    PLAYER_TURN = 'PlayerTurn'
    COMPUTER_TURN = 'ComputerTurn'
    GAME_OVER = 'GameOver'