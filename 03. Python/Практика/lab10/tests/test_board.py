import unittest

from model.entities.Board import Board
from model.entities.Cell import Cell
from model.entities.Config import Config
from model.entities.Ship import Ship
from model.entities.helpers.statuses import CellState


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.settings = Config()
        self.settings.create_default_settings()
        self.ship_border_horizontal = Ship(Cell(1,0, CellState.EMPTY), Cell(5,0, CellState.EMPTY))
        self.ship_border_vertical = Ship(Cell(1, 0, CellState.EMPTY), Cell(1, 5, CellState.EMPTY))
        self.ship_middle_horizontal = Ship(Cell(3, 2, CellState.EMPTY), Cell(6, 2, CellState.EMPTY))
        self.ship_middle_vertical = Ship(Cell(3, 2, CellState.EMPTY), Cell(3, 5, CellState.EMPTY))
        self.testBoard = Board(self.settings)
    def test_board_creation(self):

        self.assertEqual(len(self.testBoard.cells), 100)
    def test_place_ship(self):
        self.testBoard.place_ship(self.ship_middle_horizontal)
if __name__ == "__main__":
    unittest.main()