from model.entities.Cell import Cell


class Ship:
    def __init__(self):
        pass
    def set_cells(self, cells : list[Cell] ):
        self.cells = cells
    def get_cells(self):
        return self.cells
    def get_length(self):
        return len(self.cells)
    