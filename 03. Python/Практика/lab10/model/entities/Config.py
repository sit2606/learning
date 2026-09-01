import json

class Config:
    def __init__(self):
        self.size = None
        self.ships_count = None
        self.AI_difficulty = None
    pass
    def read_from_json(self, json_file: str) :
        json = json.load(open(json_file))
        self.size = json['size']
        self.ships_count = json['ships_count']
        self.AI_difficulty = json['AI_difficulty']

        pass
    def write_to_json(self, json_file: str):
        pass

