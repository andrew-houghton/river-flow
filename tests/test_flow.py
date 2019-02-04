import unittest
from data_structures.location_graph import LocationGraph
from utils.image_writer import ImageWriter
from unittest.mock import MagicMock
from algorithms.flow import flow


class TestFlow(unittest.TestCase):
    def square_list(self, n):
        return [list(range(n * i, n*(i+1))) for i in range(n)]

    def flow(self, data):
        graph = LocationGraph(data)
        writer = ImageWriter()
        writer.write = MagicMock()
        nodes_with_flow = flow(graph, writer)
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

