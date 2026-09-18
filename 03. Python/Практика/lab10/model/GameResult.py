import json
from datetime import datetime


class GameResult:
    """Хранение и управление результатами игр.

    Сохраняет/загружает результаты из JSON-файла game_results.json.

    Атрибуты:
        results (list): список результатов [{winner, loser, date}, ...]
    """

    def __init__(self):
        self.results = []

    def record(self, winner: str, loser: str):
        """Записывает результат игры.

        Args:
            winner: имя победителя
            loser: имя проигравшего
        """
        self.results.append({
            "winner": winner,
            "loser": loser,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def save_to_json(self):
        """Сохраняет все результаты в game_results.json."""
        with open('game_results.json', "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=4, ensure_ascii=False)

    def load_from_json(self):
        """Загружает результаты из game_results.json."""
        with open('game_results.json', "r", encoding="utf-8") as f:
            self.results = json.load(f)
