from enum import Enum


class CellState(Enum):
    """Состояния клетки на доске."""
    FILL = 'Fill'       # клетка занята кораблём
    EMPTY = 'Empty'     # клетка пуста
    HIT = 'Hit'         # клетка с попаданием
    MISS = 'Miss'       # клетка с промахом


class ShipState(Enum):
    """Состояния корабля."""
    FULL = 'Full'           # корабль цел
    WOUNDED = 'Wounded'     # корабль ранен
    KILLED = 'Killed'       # корабль уничтожен


class GameState(Enum):
    """Состояния игры."""
    SETUP = 'Setup'                     # расстановка кораблей
    PLAYER_TURN = 'PlayerTurn'          # ход игрока
    COMPUTER_TURN = 'ComputerTurn'      # ход компьютера
    GAME_OVER = 'GameOver'              # игра окончена
