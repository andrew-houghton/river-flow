import unittest
from unittest.mock import MagicMock

from algorithms.flow import flow
from data_structures.location_graph import LocationGraph
from utils.dummy_writer import DummyWriter


class TestFlow(unittest.TestCase):
    def square_list(self,  n):
        return [list(range(n * i, n * (i + 1))) for i in range(n)]

    def flow(self, data):
        graph = LocationGraph(data)
        num_points = sum([len(i) for i in data])
        self.assertEqual(num_points, len(graph))
        writer = DummyWriter()
        writer.update = MagicMock()
        nodes_with_flow = flow(graph, writer)
        self.assertEqual(writer.update.call_count, num_points)
        return [i.flow for i in nodes_with_flow.ascending()]

    def test_1d_flow(self):
        flows = self.flow([[1, 2, 3]])
        self.assertEqual([1, 1, 1], flows)

    def test_2d_flow_3x3(self):
        flows = self.flow(self.square_list(3))
        self.assertEqual(
            [1.4, 1.3, 1.2, 1.1, 1.0, 1.0, 1.0, 1.0, 1.0],
            flows
        )

    def test_2d_flow_4x4(self):
        flows = self.flow(self.square_list(4))
        self.assertEqual(
            [1.7060327019362067, 2.1633696299149188, 1.9024543958544868,
            1.3591260810195722, 1.555407723819194, 1.8356850250341374,
            1.5562130177514792, 1.2307692307692308, 1.0828402366863905,
            1.0769230769230769, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            flows
        )
