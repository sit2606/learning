import unittest

from model.entities.Cell import Cell
from model.entities.Ship import Ship
from model.entities.helpers.statuses import CellState


class TestShip(unittest.TestCase):
    def setUp(self):
        self.cell_1_1 = Cell(1, 1, CellState.EMPTY)
        self.cell_4_1 = Cell(4, 1, CellState.EMPTY)
        self.test_cell1 = [
            Cell(1, 1, CellState.FILL),
            Cell(1, 2, CellState.FILL),
            Cell(1,3, CellState.FILL),
            Cell(1,4, CellState.FILL)]
        self.test_cell2 = [
            Cell(2, 1, CellState.FILL),
            Cell(3, 1, CellState.FILL),
            Cell(4, 1, CellState.FILL),
            Cell(5, 1, CellState.FILL)]
        self.cell_1_1 = Cell(1, 1, CellState.EMPTY)
        self.cell_1_5 = Cell(1, 5, CellState.EMPTY)
    def test_ship_creation(self):
        ship1 = Ship(self.cell_1_1, self.cell_4_1)
        self.assertEqual(ship1.cells, self.test_cell1)
        ship2 = Ship(self.cell_4_1, self.cell_1_1)
        self.assertEqual(ship2.cells, self.test_cell1)
        ship3 = Ship(self.cell_1_1, self.cell_1_5)
        self.assertEqual(ship3.cells, self.test_cell2)
if __name__ == "__main__":
    unittest.main()

