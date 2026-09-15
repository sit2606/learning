import random
from model.entities.Board import Board
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
        remaining = board.get_remaining_ships()
        available_sizes = [size for size, count in remaining.items() if count > 0]
        if not available_sizes:
            return False
        size = random.choice(available_sizes)
        for _ in range(100):
            x, y = self.choose_cell(board)
            orientation = random.choice(['horizontal', 'vertical'])
            ship = Ship.from_head(x=x, y=y, orientation=orientation, length=size)
            if board.place_ship(ship):
                return True
        return False

    def populate_board(self, board: Board):
        while any(count > 0 for count in board.get_remaining_ships().values()):
            if not self.place_ship(board):
                board.clear_board()
