import random
from model.entities.Board import Board
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
