import unittest
import load_data
import make_graph

class TestLoad(unittest.TestCase):
    def test_data_format(self):
        data = load_data.load()
        self.assertGreater(len(data), 0, "Data should have rows")
        self.assertGreater(len(data[0]), 0, "Data should have columns")
        self.assertEqual(data.__class__, list, "Data should be a list of lists")
        self.assertEqual(data[0].__class__, list, "Columns should be list")

    def validate_item_format(self, item):
        self.assertEqual(item.__class__, float, "Data items should be floats")
        self.assertGreater(item, -100, "Heights should be between above -100m")
        self.assertLess(item, 3000, "Data items should be below 3000m")

    def test_all_item_format(self):
        data = load_data.load()
        for i in data:
            for j in i:
                self.validate_item_format(j)

    def test_first_item_format(self):
        self.validate_item_format(load_data.load()[0][0])


class TestGraph(unittest.TestCase):
    def test_create_graph(self):
        data = load_data.load()
        graph = make_graph.convert_to_graph(data)

        self.assertEqual(len(graph), 4, "All items should be converted to graph")


if __name__ == '__main__':
    unittest.main()
