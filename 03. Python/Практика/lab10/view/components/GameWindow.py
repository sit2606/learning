from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget
from pyqt6_plugins import PyQt

from view.src.GameWindow_ui import Ui_GameWindow

class GameWindow(QWidget, Ui_GameWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.on_cell_clicked = PyQt.Signal(int, int)
        self.BoardWidget.on_cell_clicked.connect(self.on_cell_clicked.emit)