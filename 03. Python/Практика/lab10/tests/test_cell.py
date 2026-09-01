import unittest

from model.entities.Cell import Cell
from model.entities.helpers.statuses import CellState


class TestCell(unittest.TestCase):
    def test_cell_creation(self):
        cell = Cell(0 , 0 , CellState.EMPTY)
        self.assertEqual(cell.x, 0)
        self.assertEqual(cell.y, 0)
        self.assertEqual(cell.state, CellState.EMPTY)
if __name__ == "__main__":
    unittest.main()

