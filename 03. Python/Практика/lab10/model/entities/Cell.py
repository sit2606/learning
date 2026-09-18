from model.entities.helpers.statuses import *


class Cell:
    """Клетка на игровом поле.

    Атрибуты:
        x (int): координата столбца
        y (int): координата строки
        state (CellState): состояние клетки
    """

    def __init__(self, x, y, state: CellState):
        self.x = x
        self.y = y
        self.state = state

    def get_coords(self):
        """Возвращает координаты клетки (x, y)."""
        return self.x, self.y

    def set_state(self, state: CellState):
        """Устанавливает состояние клетки."""
        self.state = state

    def get_state(self):
        """Возвращает текущее состояние клетки."""
        return self.state

    def __eq__(self, other):
        """Сравнение по координатам."""
        return self.x == other.x and self.y == other.y

    def __str__(self):
        """Строковое представление для ключей словаря: '(x, y)'."""
        return f'({self.x}, {self.y})'

    def __hash__(self):
        """Хеш по координатам для использования в словарях и множествах."""
        return hash((self.x, self.y))
