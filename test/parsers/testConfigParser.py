from functools import partial
import unittest
import json
import os
from src.parsers.configParser import Config, dict_config_parser, init_config_parser, obj_config_parser

class TestDictParser(unittest.TestCase):
    def test_file_load(self):
        file_path = "temp_testDictParser.txt"
        dict = {'X': 1, 'Y': 'Test', 'Z': 100}
        
        with open(file_path, 'w') as f:
            json.dump(dict, f)

        dict = dict_config_parser(file_path)

        self.assertEqual(dict["X"], 1)
        self.assertEqual(dict["Y"], "Test")
        self.assertEqual(dict["Z"], 100)

        try: 
            os.remove(file_path)
        except:
            pass


class TestInitParser(unittest.TestCase):
    def test_file_load(self):
        file_path = "temp_testInitParser.txt"
        dict = {'X': 1, 'Y': 'Test', 'Z': 100}

        with open(file_path, 'w') as f:
            json.dump(dict, f)

        obj = init_config_parser(partial(Config), config_file_path=file_path)

        self.assertIsInstance(obj, Config)
        self.assertEqual(obj.X, 1)
        self.assertEqual(obj.Y, "Test")
        self.assertEqual(obj.Z, 100)

        try: 
            os.remove(file_path)
        except:
            pass

    def test_dict_load(self):
        dict = {'A': 1, 'B': 'Test', 'C': 100}

        obj = init_config_parser(partial(Config), config_dict=dict)

        self.assertIsInstance(obj, Config)
        self.assertEqual(obj.A, 1)
        self.assertEqual(obj.B, "Test")
        self.assertEqual(obj.C, 100)


class TestObjParser(unittest.TestCase):
    def test_file_load(self):
        file_path = "temp_testObjParser.txt"
        dict = {'X': 1, 'Y': 'Test', 'Z': 100}
        
        with open(file_path, 'w') as f:
            json.dump(dict, f)

        obj = obj_config_parser(config_file_path=file_path)

        self.assertIsInstance(obj, Config)
        self.assertTrue(obj.X == 1)
        self.assertTrue(obj.Y == "Test")
        self.assertTrue(obj.Z == 100)

        try: 
            os.remove(file_path)
        except:
            pass

    def test_dict_load(self):
        dict = {'A': 1, 'B': 'Test', 'C': 100}

        obj = obj_config_parser(config_dict=dict)

        self.assertIsInstance(obj, Config)
        self.assertTrue(obj.A == 1)
        self.assertTrue(obj.B == "Test")
        self.assertTrue(obj.C == 100)


if __name__ == "__main__":
    unittest.main()