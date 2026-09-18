import unittest

from model.entities.Board import Board
from model.entities.Cell import Cell
from model.entities.Config import Config
from model.entities.Player import Player
from model.entities.Ship import Ship
from model.entities.helpers.statuses import CellState
from model.entities.helpers.exceptions import CellOccupiedError, SizeLimitError


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.settings = Config()
        self.settings.create_default_settings()
        self.test_player = Player('Tester')
        self.ship_4_horizontal = Ship(Cell(1, 0, CellState.EMPTY), Cell(4, 0, CellState.EMPTY))
        self.ship_3_vertical = Ship(Cell(1, 0, CellState.EMPTY), Cell(1, 2, CellState.EMPTY))
        self.ship_3_horizontal = Ship(Cell(3, 2, CellState.EMPTY), Cell(5, 2, CellState.EMPTY))
        self.ship_4_vertical = Ship(Cell(3, 2, CellState.EMPTY), Cell(3, 5, CellState.EMPTY))
        self.ship_not_in_board = Ship(Cell(100, 100, CellState.EMPTY), Cell(100, 103, CellState.EMPTY))
        self.testBoard = Board(self.settings, self.test_player)
    def test_board_creation(self):
        self.assertEqual(len(self.testBoard.cells), 100)
    def test_place_ship(self):
        self.assertTrue(self.testBoard.place_ship(self.ship_3_horizontal))
        with self.assertRaises(CellOccupiedError):
            self.testBoard.place_ship(self.ship_4_vertical)
        self.testBoard.clear_board()
        self.assertTrue(self.testBoard.place_ship(self.ship_4_vertical))
        self.assertTrue(self.testBoard.place_ship(self.ship_3_vertical))
        with self.assertRaises(SizeLimitError):
            self.testBoard.place_ship(self.ship_not_in_board)
        self.testBoard.clear_board()
    def test_shot(self):
        self.testBoard.place_ship(self.ship_3_horizontal)
        self.testBoard.place_ship(self.ship_4_horizontal)
        self.assertTrue(self.testBoard.shot('3','2'), CellState.HIT)
        self.assertTrue(self.testBoard.cells.get('(3, 2)').state, CellState.HIT)
        self.assertTrue(self.testBoard.shot('1', '0'), CellState.HIT)
        self.assertTrue(self.testBoard.cells.get('(1, 0)').state, CellState.HIT)
        self.assertTrue(self.testBoard.shot('0', '0'), CellState.MISS)
        self.assertTrue(self.testBoard.cells.get('(0, 0)').state, CellState.MISS)
    def test_remaining_ships_empty_board(self):
        remaining = self.testBoard.get_remaining_ships()
        self.assertEqual(remaining, {1: 4, 2: 3, 3: 2, 4: 1})

    def test_remaining_ships_after_place(self):
        ship_1 = Ship(Cell(0, 0, CellState.EMPTY), Cell(0, 0, CellState.EMPTY))
        self.testBoard.place_ship(ship_1)
        remaining = self.testBoard.get_remaining_ships()
        self.assertEqual(remaining[1], 3)
        self.assertEqual(remaining[4], 1)

    def test_remaining_ships_all_placed(self):
        for i in range(4):
            ship = Ship(Cell(0, i * 2, CellState.EMPTY), Cell(0, i * 2, CellState.EMPTY))
            self.testBoard.place_ship(ship)
        remaining = self.testBoard.get_remaining_ships()
        self.assertEqual(remaining[1], 0)

    def test_can_place_ship_size_empty_board(self):
        self.assertTrue(self.testBoard.can_place_ship_size(1))
        self.assertTrue(self.testBoard.can_place_ship_size(4))

    def test_can_place_ship_size_all_placed(self):
        for i in range(4):
            ship = Ship(Cell(0, i * 2, CellState.EMPTY), Cell(0, i * 2, CellState.EMPTY))
            self.testBoard.place_ship(ship)
        self.assertFalse(self.testBoard.can_place_ship_size(1))
        self.assertTrue(self.testBoard.can_place_ship_size(4))


if __name__ == "__main__":
    unittest.main()