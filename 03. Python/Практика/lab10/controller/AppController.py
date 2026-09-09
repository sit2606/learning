from model.entities.Game import Game
from view.components.GameWindow import GameWindow


class AppController:
    def __init__(self, game: Game, view):
        self.game = game
        self.view = view
        view.new_game_clicked.connect(self.new_game)

    def new_game(self):
        self.game_window = GameWindow()
        self.game_window.show()
        self.game_window.on_cell_clicked(self.game.make_shot)
