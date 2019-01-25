import unittest
import load_data


class TestLoad(unittest.TestCase):
    def test_data_format(self):
        data = load_data.load()
        self.assertGreater(len(data), 0, "Data should have rows")
        self.assertGreater(len(data[0]), 0, "Data should have columns")
        self.assertEqual(data.__class__, list, "Data should be a list of lists")
        self.assertEqual(data[0].__class__, list, "Columns should be list")

    def test_item_format(self):
        data = load_data.load()
        first_item = data[0][0]

        self.assertEqual(first_item.__class__, float, "Data items should be floats")
        self.assertGreater(first_item, -100, "Heights should be between above -100m")
        self.assertLess(first_item, 3000, "Data items should be below 3000m")


if __name__ == '__main__':
    unittest.main()
