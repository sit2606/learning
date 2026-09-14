from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import pyqtSignal


class BoardWidget(QWidget):
    cell_clicked = pyqtSignal(int, int)

    def __init__(self, parent=None, size=10):
        super().__init__(parent)
        self.size = size
        self.grid = [[0] * size for _ in range(size)]

    def paintEvent(self, event):
        cell_size = min(self.width(), self.height()) // self.size
        painter = QPainter(self)
        for row in range(self.size):
            for col in range(self.size):
                x = col * cell_size
                y = row * cell_size
                match self.grid[row][col]:
                    case 1:
                        painter.setBrush(QColor(100, 100, 100))
                    case 2:
                        painter.setBrush(QColor(178, 34, 34))
                    case 3:
                        painter.setBrush(QColor(128, 128, 128))
                    case _:
                        painter.setBrush(QColor(255, 255, 255))
                painter.drawRect(x, y, cell_size, cell_size)

    def mousePressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        cell_size = min(self.width(), self.height()) // self.size
        col = x // cell_size
        row = y // cell_size
        self.cell_clicked.emit(row, col)
