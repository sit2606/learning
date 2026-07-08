class cell_info:
    def __init__(self, status, age=0):
        self._status = status
        self._alive_neighbours = 0
        self._age = age

