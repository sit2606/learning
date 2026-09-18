class Player:
    """Игрок.

    Атрибуты:
        name (str): имя игрока
        wins (int): количество побед
        loses (int): количество поражений
    """

    def __init__(self, name: str):
        self.name = name
        self.wins = 0
        self.loses = 0

    def win(self):
        """Увеличивает счётчик побед."""
        self.wins += 1

    def lose(self):
        """Увеличивает счётчик поражений."""
        self.loses += 1

    def get_stats(self):
        """Возвращает статистику (победы, поражения)."""
        return self.wins, self.loses
