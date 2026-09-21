import json

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from view.src.SettingsWindow_ui import Ui_SettingsDialog


class SettingsWindow(QWidget, Ui_SettingsDialog):
    """Окно настроек игры.

    Сигналы:
        save_clicked(str, int, str): нажата кнопка Save, передаёт
            size, difficulty (индекс) и ship_sizes (JSON-строка)
        close_clicked: нажата кнопка Close
    """
    save_clicked = pyqtSignal(str, int, str)
    close_clicked = pyqtSignal()
    reset_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.AIDifficultycomboBox.addItems(["Лёгкий", "Средний", "Тяжёлый"])
        self.buttonBox.accepted.connect(self._on_save)
        self.buttonBox.rejected.connect(self._on_close)
        self.buttonBox.button(
            self.buttonBox.StandardButton.Reset
        ).clicked.connect(self._on_reset)

    def _on_save(self):
        """Собирает данные из полей и испускает save_clicked."""
        self.save_clicked.emit(
            self.get_size(),
            self.get_difficulty(),
            self.get_ship_sizes()
        )

    def _on_close(self):
        """Испускает close_clicked."""
        self.close_clicked.emit()

    def _on_reset(self):
        """Испускает reset_clicked."""
        self.reset_clicked.emit()

    def set_size(self, value):
        """Устанавливает размер поля."""
        self.SizetextEdit.setText(str(value))

    def set_difficulty(self, value):
        """Устанавливает сложность AI."""
        self.AIDifficultycomboBox.setCurrentIndex(int(value))

    def set_ship_sizes(self, ship_sizes):
        """Отображает ship_sizes в читаемом виде."""
        self.ShipCounttextEdit.setText(json.dumps(ship_sizes))

    def get_size(self):
        """Читает размер поля из поля ввода."""
        return self.SizetextEdit.toPlainText()

    def get_difficulty(self):
        """Читает сложность AI."""
        return self.AIDifficultycomboBox.currentIndex()

    def get_ship_sizes(self):
        """Читает ship_sizes из текстового поля."""
        return self.ShipCounttextEdit.toPlainText()
