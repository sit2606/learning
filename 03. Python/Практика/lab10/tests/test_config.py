import unittest
import os
from model.entities.Config import Config



class TestSettings(unittest.TestCase):
    def setUp(self):
        self.data1 = {
               "size": "10x10",
               "ships_count": 3,
               "AI_difficulty": 1,
               "player" : 'Player1',
               "ship_sizes": {1: 2, 2: 1}
       }
        self.data2 = {
            "size": "15x10",
            "ships_count": 4,
            "AI_difficulty": 1,
            "player" : 'Player2',
            "ship_sizes": {1: 3, 2: 1}
        }
    def test_create(self):
        conf = Config()
        conf.create_json(self.data1)
        self.assertTrue(os.path.exists("settings.json"))
    def test_read(self):
        conf = Config()
        conf.read_from_json()
        self.assertEqual(conf.ships_count, self.data1["ships_count"])
        self.assertEqual(conf.AI_difficulty, self.data1["AI_difficulty"])
        self.assertEqual(conf.size, self.data1["size"])
        self.assertEqual(conf.player, self.data1["player"])
        os.remove("settings.json")
    def test_read_ship_sizes(self):
        conf = Config()
        conf.create_json(self.data1)
        conf.read_from_json()
        self.assertEqual(conf.ship_sizes, {1: 2, 2: 1})
        self.assertIsInstance(list(conf.ship_sizes.keys())[0], int)
        os.remove("settings.json")
    def test_write(self):
        conf = Config()
        conf.create_json(self.data1)
        conf.size = self.data2["size"]
        conf.ships_count = self.data2["ships_count"]
        conf.AI_difficulty = self.data2["AI_difficulty"]
        conf.player = self.data2["player"]
        conf.ship_sizes = self.data2["ship_sizes"]
        conf.write_to_json()
        conf.read_from_json()
        self.assertEqual(conf.ships_count, self.data2["ships_count"])
        os.remove("settings.json")
if __name__ == "__main__":
    unittest.main()

