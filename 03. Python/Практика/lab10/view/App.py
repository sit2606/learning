import sys

from PyQt6.QtWidgets import QApplication

from controller.AppController import AppController
from model.entities.Config import Config
from model.entities.Game import Game
from model.GameResult import GameResult
from view.components.MainWindow import MainWindow


def run_gui():
    app = QApplication(sys.argv)
    config = Config()
    config.create_default_settings()
    game = Game(config)
    game_result = GameResult()
    window = MainWindow()
    controller = AppController(game, window, game_result)
    window.show()
    sys.exit(app.exec())