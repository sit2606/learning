from model.entities.Cell import Cell
from model.entities.Player import Player
from model.entities.Ship import Ship
from model.entities.Config import Config
from model.entities.helpers.statuses import CellState, ShipState


class Board:
    """Игровое поле.

    Управляет сеткой клеток, кораблями и правилами размещения/стрельбы.

    Атрибуты:
        size (str): размер поля, например '10x10'
        width (str): ширина (количество столбцов)
        height (str): высота (количество строк)
        cells (dict): словарь клеток, ключ — '(x, y)'
        ships (dict): словарь размещённых кораблей
        ship_sizes (dict): допустимые размеры кораблей {размер: количество}
        owner (Player): владелец доски
    """

    def __init__(self, settings: Config, owner: Player):
        """Создаёт пустое поле по настройкам.

        Args:
            settings: конфигурация игры (размер, корабли)
            owner: игрок-владелец доски
        """
        self.size = settings.size
        self.ships_count = settings.ships_count
        self.AI_difficulty = settings.AI_difficulty
        self.ships = {}
        self.cells = {}
        self.width, self.height = self.size.split("x")
        self.owner = owner
        self.ship_sizes = settings.ship_sizes
        x, y = 0, 0
        while y < int(self.height):
            x = 0
            while x < int(self.width):
                cell_to_add = Cell(x, y, CellState.EMPTY)
                self.cells.update({str(cell_to_add): cell_to_add})
                x += 1
            y += 1
        self.vacant_cells = self.cells

    def place_ship(self, ship: Ship):
        """Размещает корабль на доске, если позиция допустима.

        Проверяет: валидность позиции + допустимость размера.

        Args:
            ship: корабль для размещения

        Returns:
            True если корабль размещён, False если нельзя
        """
        if self.validate_ship_position(ship) and self.can_place_ship_size(ship.get_length()):
            self.ships.update({str(ship): ship})
            for cell in ship.cells:
                self.cells.update({str(cell): cell})
            return True
        else:
            return False

    def _get_neighbors(self, x: int, y: int) -> list[Cell]:
        """Возвращает список соседних клеток (8 направлений).

        Args:
            x: координата столбца
            y: координата строки

        Returns:
            список соседних клеток в пределах поля
        """
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < int(self.width) and 0 <= ny < int(self.height):
                    neighbors.append(self.cells[f"({nx}, {ny})"])
        return neighbors

    def can_place_ship_size(self, size: int) -> bool:
        """Проверяет, можно ли разместить ещё корабль данного размера.

        Args:
            size: длина корабля

        Returns:
            True если корабль такого размера ещё допустим
        """
        remaining = self.get_remaining_ships()
        return remaining.get(size, 0) > 0

    def get_remaining_ships(self) -> dict[int, int]:
        """Возвращает, сколько кораблей каждого размера ещё нужно расставить.

        Returns:
            словарь {размер: количество_оставшихся}
        """
        remaining = {}
        for size, max_count in self.ship_sizes.items():
            placed = sum(1 for ship in self.ships.values()
                         if ship.get_length() == size)
            remaining[size] = max_count - placed
        return remaining

    def clear_board(self):
        """Очищает доску: все клетки → EMPTY, все корабли удалены."""
        for cell in self.cells.values():
            cell.set_state(CellState.EMPTY)
        self.ships = {}

    def validate_ship_position(self, ship: Ship):
        """Проверяет, можно ли разместить корабль в данной позиции.

        Проверяет:
        1. Все клетки в пределах поля
        2. Все клетки пустые
        3. Нет соседних кораблей

        Args:
            ship: корабль для проверки

        Returns:
            True если позиция допустима
        """
        for cell in ship.cells:
            if not (0 <= cell.x < int(self.width) and 0 <= cell.y < int(self.height)):
                return False
            if self.cells.get(f'({str(cell.x)}, {str(cell.y)})').get_state() != CellState.EMPTY:
                return False
            for neighbor in self._get_neighbors(cell.x, cell.y):
                if neighbor.get_state() == CellState.FILL:
                    return False
        return True

    def shot(self, x: str, y: str) -> CellState:
        """Производит выстрел по клетке.

        Args:
            x: координата столбца (строка)
            y: координата строки (строка)

        Returns:
            CellState.HIT — попадание
            CellState.MISS — промах
            иное — клетка уже обстреляна
        """
        cell = self.cells.get(f'({x}, {y})')
        match cell.state:
            case CellState.EMPTY:
                cell.set_state(CellState.MISS)
                return cell.state
            case CellState.FILL:
                cell.set_state(CellState.HIT)
                self.update_board_ship_state()
                return cell.state
            case _:
                return cell.state

    def update_board_ship_state(self):
        """Удаляет уничтоженные корабли из словаря ships."""
        to_remove = []
        for ship_key, ship in self.ships.items():
            if ship.get_state() == ShipState.KILLED:
                to_remove.append(ship_key)
        for key in to_remove:
            self.ships.pop(key)

    def get_board_ship_count(self) -> int:
        """Возвращает количество живых кораблей на доске."""
        return len(self.ships)
