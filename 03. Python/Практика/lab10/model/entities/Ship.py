from model.entities.Cell import Cell
from model.entities.helpers.statuses import ShipState, CellState


class Ship:
    def __init__(self, head_cell: Cell, tail_cell: Cell):
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