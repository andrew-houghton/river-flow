import unittest
from data_structures.location_graph import LocationGraph


def load_data():
    return [
        [0.1,0.2],
        [0.3,0.4]
    ]


class TestGraph(unittest.TestCase):
    def all_connections_both_directions(self, graph):
        for node in graph.ascending():
            for i in node.links.inflow():
                self.assertTrue(node in i.links.outflow())
            for i in node.links.outflow():
                self.assertTrue(node in i.links.inflow())

    def test_create_graph(self):
        graph = LocationGraph(load_data())
        self.assertEqual(len(graph), 4, "All items should be converted to graph")
        self.all_connections_both_directions(graph)

    def test_graph_node_ordering(self):
        graph = LocationGraph(load_data())
        node_list = list(graph.ascending())
        for i in range(len(node_list) - 1):
            self.assertLessEqual(node_list[i].altitude, node_list[i + 1].altitude)

    def test_node_conversion(self):
        graph = LocationGraph([[0.1, 0.2]])
        node = graph.highest

        self.assertEqual(node.altitude, 0.2)
        self.assertEqual(node.flow, 0.0)
        self.assertEqual(node.position, {(0, 1)})
        self.assertEqual(len(list(node.links.inflow())), 0)
        self.assertEqual(len(list(node.links.outflow())), 1)
        self.assertEqual(graph.lowest, next(iter(node.links.outflow())))
        self.all_connections_both_directions(graph)

    def test_node_merging(self):
        graph = LocationGraph([[0.1, 0.2], [0.1, 0.3]])
        self.all_connections_both_directions(graph)
        self.assertEqual(len(graph), 3)

        node = graph.lowest
        self.assertEqual(node.altitude, 0.1)
        self.assertEqual(node.flow, 0.0)
        self.assertEqual(node.position, {(0, 0), (1, 0)})
        self.assertEqual(set(node.links.inflow()), {node.above, node.above.above})
        self.assertEqual(len(list(node.links.inflow())), 2)
        self.assertEqual(len(list(node.links.outflow())), 0)

    def test_multiple_merged_points(self):
        graph = LocationGraph([[2, 2, 2], [2, 1, 2], [2, 2, 2]])
        self.all_connections_both_directions(graph)
        self.assertEqual(len(graph), 2)
        self.assertEqual(graph.lowest.home, (1, 1))
        self.assertNotEqual(graph.highest.home, (1, 1))

    def test_4_merged_points(self):
        graph = LocationGraph([[2, 2], [2, 2]])
        self.all_connections_both_directions(graph)
        self.assertEqual(len(graph), 1)
        self.assertEqual(graph.highest, graph.lowest)
        self.assertIsNone(graph.highest.above)
        self.assertIsNone(graph.highest.below)
