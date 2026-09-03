from model.entities.Cell import Cell
from model.entities.Ship import Ship
from model.entities.Config import Config
from model.entities.helpers.statuses import ShotState, CellState


class Board:
    def __init__(self, settings: Config):
        self.size = settings.size
        self.ships_count = settings.ships_count
        self.AI_difficulty = settings.AI_difficulty
        self.ships = []
        self.cells = {}
        self.width, self.height = self.size.split("x")
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
        self.ships.append(ship)
        for cell in ship.cells:
            self.vacant_cells.update({str(cell): cell})
        pass
    def clear_board(self):
        for cell in self.cells:
            cell.set_state(CellState.EMPTY)
    def validate_ship_position(self, ship: Ship):
        pass
    def shot(self, x,y) -> ShotState:
        pass
    def get_ships_state(self):
        pass