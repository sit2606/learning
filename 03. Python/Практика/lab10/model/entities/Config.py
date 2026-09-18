import json

from model.entities.helpers.default_settings import DEFAULTS


class Config:
    """Конфигурация игры.

    Загружает/сохраняет настройки из JSON-файла.

    Атрибуты:
        size (str): размер поля, например '10x10'
        ships_count (int): общее количество кораблей
        ship_sizes (dict): допустимые размеры кораблей {размер: количество}
        AI_difficulty (int): сложность ИИ
        player (str): имя игрока
    """

    def __init__(self):
        self.size = None
        self.ships_count = None
        self.ship_sizes = None
        self.AI_difficulty = None
        self.data = None
        self.player = None

    def create_json(self, data: dict):
        """Записывает данные в settings.json.

        Args:
            data: словарь с настройками
        """
        self.data = data
        with open("settings.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)

    def create_default_settings(self):
        """Создаёт settings.json с настройками по умолчанию и загружает их."""
        self.data = DEFAULTS
        self.create_json(self.data)
        self.read_from_json()

    def read_from_json(self):
        """Читает настройки из settings.json и заполняет атрибуты."""
        with open("settings.json", "r") as f:
            data = json.load(f)
        self.size = data['size']
        self.ships_count = data['ships_count']
        self.AI_difficulty = data['AI_difficulty']
        self.player = data['player']
        self.ship_sizes = {int(k): v for k, v in data['ship_sizes'].items()}

    def write_to_json(self):
        """Сохраняет текущие атрибуты в settings.json."""
        self.data.update(
            {
                "size": self.size,
                "ships_count": self.ships_count,
                "AI_difficulty": self.AI_difficulty,
                "player": self.player,
                "ship_sizes": self.ship_sizes
            })
        with open("settings.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)
