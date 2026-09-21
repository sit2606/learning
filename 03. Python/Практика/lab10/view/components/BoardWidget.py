from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import pyqtSignal


class BoardWidget(QWidget):
    cell_clicked = pyqtSignal(int, int)

    def __init__(self, parent=None, rows=10, cols=10):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.grid = [[0] * cols for _ in range(rows)]

    def reset_grid(self, rows, cols):
        """Сбрасывает сетку с новым размером.

        Args:
            rows: количество строк
            cols: количество столбцов
        """
        self.rows = rows
        self.cols = cols
        self.grid = [[0] * cols for _ in range(rows)]
        self.update()

    def paintEvent(self, event):
        cell_w = self.width() // self.cols
        cell_h = self.height() // self.rows
        painter = QPainter(self)
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * cell_w
                y = row * cell_h
                match self.grid[row][col]:
                    case 1:
                        painter.setBrush(QColor(100, 100, 100))
                    case 2:
                        painter.setBrush(QColor(178, 34, 34))
                    case 3:
                        painter.setBrush(QColor(128, 128, 128))
                    case 4:
                        painter.setBrush(QColor(0, 255, 127))
                    case 5:
                        painter.setBrush(QColor(0, 128, 0))
                    case _:
                        painter.setBrush(QColor(255, 255, 255))
                painter.drawRect(x, y, cell_w, cell_h)

    def mousePressEvent(self, event):
        cell_w = self.width() // self.cols
        cell_h = self.height() // self.rows
        col = event.pos().x() // cell_w
        row = event.pos().y() // cell_h
        self.cell_clicked.emit(row, col)
