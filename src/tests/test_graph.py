import unittest
from data_structures.location_graph import LocationGraph


def load_data():
    return [
        [0.1,0.2],
        [0.3,0.4]
    ]


class TestGraph(unittest.TestCase):
    def test_create_graph(self):
        graph = LocationGraph(load_data())
        self.assertEqual(len(graph), 4, "All items should be converted to graph")

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
        self.assertEqual(len(node.outflow), 1)
        self.assertEqual(graph.lowest, next(iter(node.outflow)))

    def test_node_object_is_clean(self):
        graph = LocationGraph([[0.1, 0.2]])
        node = graph.highest
        self.assertEqual(
            set(node.__dict__.keys()),
            {'outflow', 'altitude', 'flow', 'is_border', 'above', 'below', 'position'}
            )

    def test_node_merging(self):
        graph = LocationGraph([[0.1, 0.2], [0.1, 0.3]])
        self.assertEqual(len(graph), 3)

        top = graph.highest
        self.assertEqual(top.position, {(1,1)})
        self.assertEqual(len(top.outflow), 2)
        self.assertEqual(top.altitude, 0.3)
        self.assertEqual(top.is_border, True)

        middle = top.below
        self.assertEqual(middle.position, {(0, 1)})
        self.assertEqual(len(middle.outflow), 1)
        self.assertEqual(middle.altitude, 0.2)
        self.assertEqual(middle.is_border, True)

        bottom = graph.lowest
        self.assertEqual(bottom.position, {(0, 0), (1,0)})
        self.assertEqual(bottom.altitude, 0.1)
        self.assertEqual(bottom.position, {(0, 0), (1, 0)})
        self.assertEqual(len(bottom.outflow), 0)

    def test_multiple_merged_points(self):
        graph = LocationGraph([[2, 2, 2], [2, 1, 2], [2, 2, 2]])
        self.assertEqual(len(graph), 2)

        top = graph.highest
        self.assertEqual(
            top.position,
            {(0,0),(0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2)}
            )
        self.assertEqual(top.altitude, 2)
        self.assertEqual(len(top.outflow), 1)
        self.assertEqual(top.is_border, True)

        bottom = graph.lowest
        self.assertEqual(bottom.position, {(1, 1)})
        self.assertEqual(bottom.altitude, 1)
        self.assertEqual(len(bottom.outflow), 0)
        self.assertEqual(bottom.is_border, False)
        

    def test_4_merged_points(self):
        graph = LocationGraph([[2, 2], [2, 2]])
        self.assertEqual(len(graph), 1)
        self.assertEqual(graph.highest, graph.lowest)
        self.assertIsNone(graph.highest.above)
        self.assertIsNone(graph.highest.below)
        self.assertEqual(graph.highest.outflow, [])

if __name__ == '__main__':
    unittest.main()
