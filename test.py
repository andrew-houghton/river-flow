import unittest
import load_data
import time
from flow import simulate_flow
from image_writer import ImageWriter
from unittest.mock import MagicMock
from map import LocationGraph


class TestLoad(unittest.TestCase):
    def test_data_format(self):
        data = load_data.load()
        self.assertGreater(len(data), 0, "Data should have rows")
        self.assertGreater(len(data[0]), 0, "Data should have columns")
        self.assertEqual(data.__class__, list,
                         "Data should be a list of lists")
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
        graph = LocationGraph(load_data.load())
        self.assertEqual(graph.length(), 4, "All items should be converted to graph")

    def test_graph_node_ordering(self):
        graph = LocationGraph(load_data.load())
        node_list = list(graph.ascending())
        for i in range(len(node_list) - 1):
            self.assertLessEqual(node_list[i].altitude, node_list[i + 1].altitude)

    def test_node_conversion(self):
        graph = LocationGraph([[0.1, 0.2]])
        node = graph.last

        self.assertEqual(node.altitude, 0.2)
        self.assertEqual(node.flow, 0.0)
        self.assertEqual(node.original_location, {(0, 1)})
        self.assertEqual(len(node.inflow), 0)
        self.assertEqual(len(node.outflow), 1)
        self.assertEqual(graph.first, next(iter(node.outflow)))

    def test_node_merging(self):
        graph = LocationGraph([[0.1, 0.2], [0.1, 0.3]])
        self.assertEqual(graph.length(), 3)

        node = graph.first
        self.assertEqual(node.altitude, 0.1)
        self.assertEqual(node.flow, 0.0)
        self.assertEqual(node.original_location, {(0, 0), (1, 0)})
        self.assertEqual(node.inflow, {node.next, node.next.next})
        self.assertEqual(len(node.inflow), 2)
        self.assertEqual(len(node.outflow), 0)


class TestFlooding(unittest.TestCase):
    def is_border_location(self, size, x, y):
        return x == 0 or y == 0 or x == size-1 or y == size-1

    def any_border_location(self, locations, size):
        for i in locations:
            if self.is_border_location(size, *i):
                return True
        return False

    def test_border_exists_small(self):
        graph = LocationGraph([[1, 2, 3], [1, 4, 3], [1, 2, 3]])
        for node in graph.ascending():
            node_touches_border = self.any_border_location(
                node.original_location, 3)
            self.assertEqual(node_touches_border, node.border)

    def test_border_exists_large(self):
        size = 50
        graph = LocationGraph([list(range(size)) for i in range(size)])
        for node in graph.ascending():
            node_touches_border = self.any_border_location(
                node.original_location, size)
            self.assertEqual(node_touches_border, node.border)


class TestFlow(unittest.TestCase):
    def square_list(self, n):
        return [list(range(n * i, n*(i+1))) for i in range(n)]

    def flow(self, data):
        graph = LocationGraph(data)
        writer = ImageWriter()
        writer.write = MagicMock()
        nodes_with_flow = simulate_flow(graph, writer)
        self.assertEqual(writer.write.call_count, sum([len(i) for i in data]))
        return [i.flow for i in nodes_with_flow.ascending()]

    def test_1d_flow(self):
        flows = self.flow([[1, 2, 3]])
        self.assertEqual([1, 1, 1], flows)

    def test_2d_flow(self):
        flows = self.flow(self.square_list(3))
        self.assertEqual([1.0, 1.75, 1.0, 1.25, 1.0,
                          1.0, 1.0, 1.0, 1.0], flows)

    def test_large_flow(self):
        flows = self.flow(self.square_list(5))
        expected = [1.0, 3.943672839506173, 3.7662037037037037, 3.1064814814814814, 1.0, 1.5887345679012346, 3.5324074074074074, 3.3194444444444446, 2.5277777777777777, 1.0,
                    1.3958333333333333, 2.375, 2.2777777777777777, 1.8333333333333335, 1.0, 1.199074074074074, 1.1944444444444444, 1.1666666666666667, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        self.assertEqual(expected, flows)


if __name__ == '__main__':
    unittest.main()
