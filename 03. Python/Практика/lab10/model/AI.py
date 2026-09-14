import random
from model.entities.Board import Board
from model.entities.Cell import Cell
from model.entities.Game import Game
from model.entities.Ship import Ship
from model.entities.helpers.statuses import CellState


class AI:
    def __init__(self, difficulty: int):
        self.difficulty = difficulty
    def choose_cell(self, board: Board) -> tuple[int, int]:
        available = []
        for cell in board.cells.values():
            if cell.get_state() == CellState.EMPTY:
                available.append((cell.x, cell.y))
        return random.choice(available)
    def place_ship(self, board: Board):
        x,y  = self.choose_cell(board)
        head = Cell(x,y, CellState.EMPTY)
        orientation = ['horizontal', 'vertical']

        ship = Ship.from_head(head, orientation = random.choice(orientation))
