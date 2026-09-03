import unittest

from model.entities.Cell import Cell
from model.entities.Ship import Ship
from model.entities.helpers.statuses import CellState, ShipState


class TestShip(unittest.TestCase):
    def setUp(self):
        self.cell_1_1 = Cell(1, 1, CellState.EMPTY)
        self.cell_4_1 = Cell(4, 1, CellState.EMPTY)
        self.test_cell1 = [
            Cell(1, 1, CellState.FILL),
            Cell(2, 1, CellState.FILL),
            Cell(3,1, CellState.FILL),
            Cell(4,1, CellState.FILL)]
        self.test_cell2 = [
            Cell(1, 1, CellState.FILL),
            Cell(1, 2, CellState.FILL),
            Cell(1, 3, CellState.FILL),
            Cell(1, 4, CellState.FILL)]
        self.cell_1_1 = Cell(1, 1, CellState.EMPTY)
        self.cell_1_4 = Cell(1, 4, CellState.EMPTY)
    def test_ship_creation(self):
        ship1 = Ship(self.cell_1_1, self.cell_4_1)
        self.assertEqual(ship1.cells, self.test_cell1)
        ship2 = Ship(self.cell_4_1, self.cell_1_1)
        self.assertEqual(ship2.cells, self.test_cell1)
        ship3 = Ship(self.cell_1_1, self.cell_1_4)
        self.assertEqual(ship3.cells, self.test_cell2)
    def test_ship_length(self):
        ship1 = Ship(self.cell_1_1, self.cell_1_4)
        self.assertEqual(ship1.get_length(), 4)
        ship1 = Ship(self.cell_1_1, self.cell_1_1)
        self.assertEqual(ship1.get_length(), 1)
    def test_ship_status(self):
        ship1 = Ship(self.cell_1_1, self.cell_1_4)
        ship1.cells[0].set_state(CellState.HIT)
        self.assertEqual(ShipState.WOUNDED, ship1.get_state())
        ship1 = Ship(self.cell_1_1, self.cell_1_4)
        self.assertEqual(ShipState.FULL, ship1.get_state())
if __name__ == "__main__":
    unittest.main()

