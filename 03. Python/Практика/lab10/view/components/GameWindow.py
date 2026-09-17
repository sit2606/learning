from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from view.src.GameWindow_ui import Ui_GameWindow


class GameWindow(QWidget, Ui_GameWindow):
    cell_clicked = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.BoardWidget.cell_clicked.connect(self.on_cell_clicked)
        self.CommandpushButton.setEnabled(False)
        self.CommandpushButton.setText('Начать игру')
        self.CommandpushButton.clicked.connect(self.command_button_clicked)
    def on_cell_clicked(self, row, col):
        self.cell_clicked.emit(row, col)
    def command_button_clicked(self):
        pass
    def set_status_text(self, text):
        self.InstructionLabellabel.setText(text)
    def enable_command_button(self): 
        self.CommandpushButton.setEnabled(True)
