import json
import os
from datetime import datetime


class GameResult:
    def __init__(self):
        self.results = []

    def record(self, winner: str, loser: str):
        self.results.append({
            "winner": winner,
            "loser": loser,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })



    def save_to_json(self, json_file: str):
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=4, ensure_ascii=False)

    def load_from_json(self, json_file: str):
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as f:
                self.results = json.load(f)
