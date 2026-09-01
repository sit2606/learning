from model.entities.Cell import Cell
from model.entities.helpers.statuses import ShipState


class Ship:
    def __init__(self, head_cell: Cell, tail_cell: Cell):
        self.head_cell = head_cell
        self.tail_cell = tail_cell
        if self.head_cell.x == self.tail_cell.x:
            self.orientation = 'horizontal'
            first = max(self.head_cell.y, self.tail_cell.y)
            second = min(self.head_cell.x, self.tail_cell.x)
        else:
            self.orientation = 'vertical'
            first = max(self.head_cell.x, self.tail_cell.x)
            second = min(self.head_cell.y, self.tail_cell.y)
        match self.orientation:
            case 'horizontal':
                print('horizontal')
            case 'vertical':
                print('vertical')
    def set_cells(self, cells : list[Cell] ):
        self.cells = cells
    def get_cells(self):
        return self.cells
    def get_length(self):
        return len(self.cells)
    def get_state(self) -> ShipState:
        pass