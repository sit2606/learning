from model.entities.Game import Game
from model.entities.helpers.statuses import CellState
from view.components.GameWindow import GameWindow


class AppController:
    def __init__(self, game: Game, view):
        self.game = game
        self.view = view
        self.view.new_game_clicked.connect(self.new_game)
        self.game_window = GameWindow()
        self.game_window.cell_clicked.connect(self.on_cell_clicked)
    def new_game(self):
        self.game_window.show()
    def on_cell_clicked(self, row, col):
        result = self.game.make_shot(row, col)
        if result == CellState.HIT:
            self.game_window.BoardWidget.grid[row][col] = 2  # или 2 для красного
        elif result == CellState.MISS:
            self.game_window.BoardWidget.grid[row][col] = 3  # или 3 для синего
        self.game_window.BoardWidget.update()

