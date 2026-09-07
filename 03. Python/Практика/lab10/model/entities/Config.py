import json

from model.entities.helpers.default_settings import DEFAULTS


class Config:
    def __init__(self):
        self.size = None
        self.ships_count = None
        self.AI_difficulty = None
        self.data = None
        self.player = None
    def create_json(self, data : dict):
        self.data = data
        with open("settings.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)
    def create_default_settings(self):
        self.data = DEFAULTS
        self.create_json(self.data)
        self.read_from_json()
    def read_from_json(self) :
        with open("settings.json", "r") as f:
            data = json.load(f)
        self.size = data['size']
        self.ships_count = data['ships_count']
        self.AI_difficulty = data['AI_difficulty']
        self.player = data['player']
    def write_to_json(self):
        self.data.update(
            {
                "size": self.size,
                "ships_count": self.ships_count,
                "AI_difficulty": self.AI_difficulty,
                "player": "Player1"
                          })
        with open("settings.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)


