from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from view.src.SettingsWindow_ui import Ui_SettingsDialog


class SettingsWindow(QWidget, Ui_SettingsDialog):
    """Окно настроек игры.

    Сигналы:
        save_clicked: нажата кнопка Save
        close_clicked: нажата кнопка Close
    """
    save_clicked = pyqtSignal()
    close_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.test)
        self.AIDifficultycomboBox.addItems(["Лёгкий", "Средний", "Тяжёлый"])
        self.buttonBox.rejected.connect(self.close_clicked)

    def set_size(self, value):
        """Устанавливает размер поля."""
        self.SizetextEdit.setText(str(value))
    def test(self):
        self.get_ship_sizes()
    def set_difficulty(self, value):
        """Устанавливает сложность AI."""
        self.AIDifficultycomboBox.setCurrentIndex(int(value))

    def set_ship_sizes(self, ship_sizes):
        """Отображает ship_sizes в читаемом виде."""
        self.ShipCounttextEdit.setText(ship_sizes)

    def get_size(self):
        """Читает размер поля из поля ввода."""
        return self.SizetextEdit.toPlainText()

    def get_difficulty(self):
        """Читает сложность AI."""
        return self.AIDifficultycomboBox.currentIndex()

    def get_ship_sizes(self):
        """Читает ship_sizes из текстового поля."""
        return self.ShipCounttextEdit.toPlainText()
