import unittest
from data_structures.location_graph import LocationGraph
from algorithms.flood import flood

class TestFlooding(unittest.TestCase):
    def all_nodes_have_outflow(self, nodes):
        for node in nodes:
            if not node.border and len(node.outflow)==0:
                return False
        return True

    def is_border_location(self, size, x, y):
        return x == 0 or y == 0 or x == size-1 or y == size-1

    def any_border_location(self, locations, size):
        for i in locations:
            if self.is_border_location(size, *i):
                return True
        return False

    # def test_border_exists_small(self):
    #     graph = LocationGraph([[1, 2, 3], [1, 4, 3], [1, 2, 3]])
    #     for node in graph.ascending():
    #         node_touches_border = self.any_border_location(
    #             node.original_location, 3)
    #         self.assertEqual(node_touches_border, node.border)

    # def test_border_exists_large(self):
    #     size = 50
    #     graph = LocationGraph([list(range(size)) for i in range(size)])
    #     for node in graph.ascending():
    #         node_touches_border = self.any_border_location(
    #             node.original_location, size)
    #         self.assertEqual(node_touches_border, node.border)

    def test_one_point_is_flooded(self):
        graph = LocationGraph([[2,2,2],[2,1,2],[2,2,2]])
        print(graph)
        self.assertEqual(graph.length(), 2)
        flood(graph.ascending())
        self.assertEqual(graph.length(), 1)

    def test_one_lake_flooded(self):
        pass

    def test_two_lakes_flooded(self):
        pass

    def test_large_lake(self):
        pass