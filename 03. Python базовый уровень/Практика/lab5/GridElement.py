class grid_element:
    def __init__(self, x_coordinate, y_coordinate, status):
        self._x = x_coordinate
        self._y = y_coordinate
        self._status = status
        self._alive_naighbours = 0

