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
    def get_cells(self):
        return self.cells
    def get_length(self):
        return len(self.cells)
    def get_state(self) -> ShipState:
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
