class Cell:
    def __init__(self, x,y, state):
        self.x = x
        self.y = y
        self.state = state
    def get_coords(self):
        return self.x, self.y
    def set_state(self, state):
        self.state = state
    def get_state(self):
        return self.state
    