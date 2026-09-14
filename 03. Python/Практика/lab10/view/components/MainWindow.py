from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow

from view.src.MainWindow_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    new_game_clicked = pyqtSignal()
    settings_clicked = pyqtSignal()
    leaderboard_clicked = pyqtSignal()
    exit_clicked = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.NewGame_pushButton.clicked.connect(self.on_new_game_clicked)
        self.Settings_pushButton.clicked.connect(self.settings_clicked)
        self.Leaderboard_pushButton.clicked.connect(self.leaderboard_clicked)
        self.Exit_pushButton.clicked.connect(self.exit_clicked)
    def on_new_game_clicked(self):
        self.new_game_clicked.emit()
    