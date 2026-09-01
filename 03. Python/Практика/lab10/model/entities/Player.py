class Player():
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.loses = 0
    def win(self):
        self.wins += 1
    def lose(self):
        self.loses += 1
    def get_stats(self):
        return self.wins, self.loses
