import unittest
import os
from model.entities.Config import Config



class TestSettings(unittest.TestCase):
    def setUp(self):
        self.data1 = {
               "size": "10x10",
               "ships_count": 3,
               "AI_difficulty": 1
       }
        self.data2 = {
            "size": "15x10",
            "ships_count": 4,
            "AI_difficulty": 1
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
        os.remove("settings.json")
    def test_write(self):
        conf = Config()
        conf.create_json(self.data1)
        conf.data = self.data2
        conf.write_to_json()
        conf.read_from_json()
        self.assertEqual(conf.ships_count, self.data2["ships_count"])
        os.remove("settings.json")
if __name__ == "__main__":
    unittest.main()

