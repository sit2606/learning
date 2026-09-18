from model.entities.Cell import Cell
from model.entities.helpers.statuses import ShipState, CellState


class Ship:
    """Корабль на игровом поле.

    Создаётся из двух клеток — головы и хвоста.
    Автоматически определяет ориентацию и заполняет промежуточные клетки.

    Атрибуты:
        head_cell (Cell): начальная клетка
        tail_cell (Cell): конечная клетка
        orientation (str): 'horizontal' или 'vertical'
        cells (list[Cell]): все клетки корабля
    """

    def __init__(self, head_cell: Cell, tail_cell: Cell):
        """Создаёт корабль из двух крайних клеток.

        Args:
            head_cell: начальная клетка корабля
            tail_cell: конечная клетка корабля
        """
        self.head_cell = head_cell
        self.tail_cell = tail_cell
        if head_cell.x == tail_cell.x:
            self.orientation = 'vertical'
            self.cells = [Cell(head_cell.x, y, CellState.FILL)
                          for y in range(min(head_cell.y, tail_cell.y),
                                         max(head_cell.y, tail_cell.y) + 1)]
        else:
            self.orientation = 'horizontal'
            self.cells = [Cell(x, head_cell.y, CellState.FILL)
                          for x in range(min(head_cell.x, tail_cell.x),
                                         max(head_cell.x, tail_cell.x) + 1)]

    @classmethod
    def from_head(cls, x, y, orientation, length):
        """Альтернативный конструктор: создаёт корабль из начальной точки.

        Используется AI для случайной расстановки.

        Args:
            x: координата столбца начальной клетки
            y: координата строки начальной клетки
            orientation: 'horizontal' или 'vertical'
            length: длина корабля

        Returns:
            Ship: экземпляр корабля
        """
        if orientation == 'horizontal':
            head = Cell(x, y, CellState.FILL)
            tail = Cell(x + length - 1, y, CellState.FILL)
        else:
            head = Cell(x, y, CellState.FILL)
            tail = Cell(x, y + length - 1, CellState.FILL)
        return cls(head, tail)

    def get_cells(self):
        """Возвращает список всех клеток корабля."""
        return self.cells

    def get_length(self):
        """Возвращает длину корабля."""
        return len(self.cells)

    def get_state(self) -> ShipState:
        """Возвращает состояние корабля на основе HP клеток.

        Returns:
            ShipState.FULL — корабль цел
            ShipState.WOUNDED — есть попадания, но не все
            ShipState.KILLED — все клетки подбиты
        """
        total_hp = self.get_length()
        for cell in self.cells:
            if cell.state == CellState.HIT:
                total_hp -= 1
        if total_hp == 0:
            return ShipState.KILLED
        if total_hp == self.get_length():
            return ShipState.FULL
        else:
            return ShipState.WOUNDED

    def __str__(self):
        return f'{self.head_cell}: {self.tail_cell}'
