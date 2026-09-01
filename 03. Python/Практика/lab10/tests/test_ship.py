import unittest

from model.entities.Cell import Cell
from model.entities.Ship import Ship
from model.entities.helpers.statuses import CellState


class TestShip(unittest.TestCase):
    def setUp(self):
        self.cell_1_1 = Cell(1, 1, CellState.EMPTY)
        self.cell_4_1 = Cell(4, 1, CellState.EMPTY)
    def test_ship_creation(self):
        ship = Ship(self.cell_1_1, self.cell_4_1)
if __name__ == "__main__":
    unittest.main()

