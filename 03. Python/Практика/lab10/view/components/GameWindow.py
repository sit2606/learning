from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from view.src.GameWindow_ui import Ui_GameWindow


class GameWindow(QWidget, Ui_GameWindow):
    player_board_clicked = pyqtSignal(int, int)
    enemy_board_clicked = pyqtSignal(int, int)
    command_button_clicked = pyqtSignal()
    switch_mode_clicked = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.PlayerBoard.cell_clicked.connect(self.player_board_clicked)
        self.EnemyBoard.cell_clicked.connect(self.enemy_board_clicked)

        self.CommandpushButton.setEnabled(False)
        self.CommandpushButton.setText('Начать игру')
        self.CommandpushButton.clicked.connect(self.command_clicked)
        self.SwitchModeButton.clicked.connect(self.dev_switch_mode)
        self.SwitchModeButton.setVisible(False)
    def command_clicked(self):
        self.command_button_clicked.emit()
    def dev_switch_mode(self):
        self.switch_mode_clicked.emit()
    def set_status_text(self, text):
        self.PlayerBoardLabel.setText(text)
    def set_information_text(self, text):
        """Обновляет текст в InformationBrowser."""
        self.InformationBrowser.setText(text)

    def enable_command_button(self):
        self.CommandpushButton.setEnabled(True)

    def hide_command_button(self):
        self.CommandpushButton.setVisible(False)

    def reset_boards(self, rows, cols):
        """Сбрасывает обе доски с указанным размером сетки.

        Args:
            rows: количество строк
            cols: количество столбцов
        """
        self.PlayerBoard.reset_grid(rows, cols)
        self.EnemyBoard.reset_grid(rows, cols)
