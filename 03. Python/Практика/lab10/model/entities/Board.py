from model.entities.Cell import Cell
from model.entities.Player import Player
from model.entities.Ship import Ship
from model.entities.Config import Config
from model.entities.helpers.statuses import  CellState, ShipState


class Board:
    def __init__(self, settings: Config, owner : Player):
        self.size = settings.size
        self.ships_count = settings.ships_count
        self.AI_difficulty = settings.AI_difficulty
        self.ships = {}
        self.cells = {}
        self.width, self.height = self.size.split("x")
        self.owner = owner
        self.ship_sizes = settings.ship_sizes
        x,y = 0,0
        while y< int(self.height):
            x = 0
            while x  < int(self.width):
                cell_to_add = Cell(x, y, CellState.EMPTY)
                self.cells.update({str(cell_to_add): cell_to_add})
                x += 1
            y += 1
        self.vacant_cells = self.cells
    def place_ship(self, ship: Ship):
        if self.validate_ship_position(ship) and self.can_place_ship_size(ship.get_length()):
            self.ships.update({str(ship): ship})
            for cell in ship.cells:
                self.cells.update({str(cell): cell})
            return True
        else:
            return False
    def _get_neighbors(self, x: int, y: int) -> list[Cell]:
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # саму клетку пропускаем
                nx, ny = x + dx, y + dy
                if 0 <= nx < int(self.width) and 0 <= ny < int(self.height):
                    neighbors.append(self.cells[f"({nx}, {ny})"])
        return neighbors
    def can_place_ship_size(self, size: int) -> bool:
        remaining = self.get_remaining_ships()
        return remaining.get(size, 0) > 0
    def get_remaining_ships(self) -> dict[int, int]:
        remaining = {}
        for size, max_count in self.ship_sizes.items():
            placed = sum(1 for ship in self.ships.values()
                         if ship.get_length() == size)
            remaining[size] = max_count - placed
        return remaining
    def clear_board(self):
        for cell in self.cells.values():
            cell.set_state(CellState.EMPTY)
        self.ships = {}
    def validate_ship_position(self, ship: Ship):
        for cell in ship.cells:
            # 1. Клетка в пределах поля?
            if not (0 <= cell.x < int(self.width) and 0 <= cell.y < int(self.height)):
                return False
            # 2. Клетка пустая?
            if self.cells.get(f'({str(cell.x)}, {str(cell.y)})').get_state() != CellState.EMPTY:
                return False
            # 3. Соседи не содержат кораблей?
            for neighbor in self._get_neighbors(cell.x, cell.y):
                if neighbor.get_state() == CellState.FILL:
                    return False
        return True
    def shot(self, x: str,y : str) -> CellState:
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
        to_remove = []
        for ship_key, ship in self.ships.items():
            if ship.get_state() == ShipState.KILLED:
                to_remove.append(ship_key)
        for key in to_remove:
            self.ships.pop(key)
    def get_board_ship_count(self) -> int:
        return len(self.ships)

