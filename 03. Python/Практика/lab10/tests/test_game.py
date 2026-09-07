import unittest

from model.entities.Cell import Cell
from model.entities.Config import Config
from model.entities.Ship import Ship
from model.entities.Game import Game
from model.entities.helpers.statuses import CellState, GameState


class TestGame(unittest.TestCase):
    def setUp(self):
        self.settings = Config()
        self.settings.create_default_settings()
        self.settings.player = 'Player1'
        self.game = Game(self.settings)
        self.ship1 = Ship(Cell(0, 0, CellState.EMPTY), Cell(2, 0, CellState.EMPTY))
        self.ship2 = Ship(Cell(0, 0, CellState.EMPTY), Cell(2, 0, CellState.EMPTY))

    def test_initial_state(self):
        self.assertEqual(self.game.get_state(), GameState.SETUP)
        self.assertEqual(self.game.current_player.name, 'Player1')

    def test_place_ship_setup(self):
        self.assertTrue(self.game.place_ship(self.ship1))
        self.assertEqual(self.game.board1.get_board_ship_count(), 1)

    def test_can_place_ship(self):
        self.assertTrue(self.game.can_place_ship(self.ship1))
        self.game.place_ship(self.ship1)
        self.assertFalse(self.game.can_place_ship(self.ship2))

    def test_start_game(self):
        self.game.start_game()
        self.assertEqual(self.game.get_state(), GameState.PLAYER_TURN)

    def test_switch_turn(self):
        self.game.start_game()
        self.assertEqual(self.game.get_state(), GameState.PLAYER_TURN)
        self.game.switch_turn()
        self.assertEqual(self.game.get_state(), GameState.COMPUTER_TURN)
        self.assertEqual(self.game.current_player.name, 'Player2')
        self.game.switch_turn()
        self.assertEqual(self.game.get_state(), GameState.PLAYER_TURN)
        self.assertEqual(self.game.current_player.name, 'Player1')

    def test_make_shot_hit(self):
        self.game.place_ship(self.ship1)
        self.game.start_game()
        self.game.switch_turn()
        result = self.game.make_shot(0, 0)
        self.assertEqual(result, CellState.HIT)

    def test_make_shot_miss(self):
        self.game.place_ship(self.ship1)
        self.game.start_game()
        self.game.switch_turn()
        result = self.game.make_shot(5, 5)
        self.assertEqual(result, CellState.MISS)

    def test_is_game_over(self):
        self.game.place_ship(self.ship1)
        self.game.start_game()
        self.game.switch_turn()
        self.assertFalse(self.game.is_game_over())
        self.game.make_shot(0, 0)
        self.game.make_shot(1, 0)
        self.game.make_shot(2, 0)
        self.game.board1.update_board_ship_state()
        self.assertTrue(self.game.is_game_over())

    def test_get_winner(self):
        self.game.place_ship(self.ship1)
        ship_for_board2 = Ship(Cell(5, 5, CellState.EMPTY), Cell(7, 5, CellState.EMPTY))
        self.game.board2.place_ship(ship_for_board2)
        self.game.start_game()
        self.game.switch_turn()
        self.assertEqual(self.game.get_winner(), 'The game is still on!')
        self.game.make_shot(0, 0)
        self.game.make_shot(1, 0)
        self.game.make_shot(2, 0)
        self.game.board1.update_board_ship_state()
        self.assertEqual(self.game.get_winner(), 'Player2')


if __name__ == "__main__":
    unittest.main()
