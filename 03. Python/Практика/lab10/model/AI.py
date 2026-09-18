import random
from model.entities.Board import Board
from model.entities.Ship import Ship
from model.entities.helpers.statuses import CellState


class AI:
    """Искусственный интеллект для игры в морской бой.

    Отвечает за:
    - выбор клетки для выстрела (choose_cell)
    - расстановку кораблей (place_ship, populate_board)

    Атрибуты:
        difficulty (int): уровень сложности ИИ
    """

    def __init__(self, difficulty: int):
        self.difficulty = difficulty

    def choose_cell(self, board: Board) -> tuple[int, int]:
        """Выбирает случайную пустую клетку для выстрела.

        Args:
            board: доска противника

        Returns:
            кортеж (x, y) — координаты клетки
        """
        available = []
        for cell in board.cells.values():
            if cell.get_state() == CellState.EMPTY:
                available.append((cell.x, cell.y))
        return random.choice(available)

    def place_ship(self, board: Board):
        """Пытается разместить один случайный корабль.

        Выбирает случайный размер из оставшихся, случайную позицию
        и ориентацию. Пробует до 100 раз.

        Args:
            board: доска для размещения

        Returns:
            True если корабль размещён, False если не удалось
        """
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
        """Расставляет все корабли на доске случайным образом.

        Если не удалось разместить очередной корабль — очищает доску
        и начинает расстановку заново.

        Args:
            board: доска для заполнения
        """
        while any(count > 0 for count in board.get_remaining_ships().values()):
            if not self.place_ship(board):
                board.clear_board()
