from model.entities.Board import Board
from model.entities.Config import Config
from model.entities.Player import Player
from model.entities.helpers.statuses import GameState,  CellState
from model.AI import AI


class Game:
    def __init__(self, config: Config):
        self.config = config
        self.player1 = Player('Player1')
        self.player2 = Player('Player2')
        self.board1 = Board(config, self.player1)
        self.board2 = Board(config, self.player2)
        self.state = GameState.SETUP
        self.current_player = self.player1
        self.current_board = self.board1
        self.ai = AI(config.AI_difficulty)
    # === Состояние игры ===
    def get_state(self) -> GameState:
        return self.state
    def switch_turn(self):
        if self.state == GameState.PLAYER_TURN:
            self.state = GameState.COMPUTER_TURN
            self.current_board = self.board2
            self.current_player = self.current_board.owner
        elif self.state == GameState.COMPUTER_TURN:
            self.state = GameState.PLAYER_TURN
            self.current_board = self.board1
            self.current_player = self.current_board.owner
    def is_game_over(self) -> bool:
        return self._get_opponent_board().get_board_ship_count() == 0
    def place_ship(self, ship) -> bool:
        return self.current_board.place_ship(ship)

    def can_place_ship(self, ship) -> bool:
        return self.current_board.validate_ship_position(ship)

    def can_place_ship_size(self, size: int) -> bool:
        placed = sum(1 for ship in self.current_board.ships.values()
                     if ship.get_length() == size)
        return placed < self.config.ship_sizes.get(size, 0)

    def start_game(self):
        player = self.config.player
        if player == 'Player1':
            self.current_player = self.player1
            self.current_board = self.board1
            self.state = GameState.PLAYER_TURN
        elif player == 'Player2':
            self.current_player = self.player2
            self.current_board = self.board2
            self.state = GameState.COMPUTER_TURN
    def make_shot(self, x: int, y: int) -> CellState:
        return self._get_opponent_board().shot(str(x), str(y))
    def get_winner(self) -> str:
        if self.board1.get_board_ship_count() == 0:
            return self.board2.owner.name
        elif self.board2.get_board_ship_count() == 0:
            return self.board1.owner.name
        else:
            return 'The game is still on!'

    def _get_opponent_board(self) -> Board:
        if self.current_board == self.board1:
            return self.board2
        return self.board1

    def computer_turn(self) -> CellState:
        x, y = self.ai.choose_cell(self._get_opponent_board())
        result = self.make_shot(x, y)
        self.switch_turn()
        return result