import unittest

from data_structures.node import Node


class TestNodeMerging(unittest.TestCase):
    @staticmethod
    def set_flow(a, b):
        a.inflow.add(b)
        b.outflow.add(a)

    @staticmethod
    def sample_node(altitude):
        coordinates = (0, altitude)
        n = Node()
        n.altitude = altitude
        n.home = coordinates
        n.position.add(coordinates)
        return n

    @staticmethod
    def connect_in_order(*args):
        for i in range(len(args) - 1):
            args[i].next = args[i + 1]
            args[i + 1].prev = args[i]

    def test_simple_case(self):
        a, b = self.sample_node(1), self.sample_node(2)
        self.set_flow(a, b)

        self.connect_in_order(a, b)

        self.assertEqual(a.above, b)
        self.assertIsNone(b.above)
        self.assertEqual(b.below, a)
        self.assertIsNone(a.below)

        a.merge(b)

        self.assertEqual(a.position, {(0, 1), (0, 2)})
        self.assertEqual(a.altitude, 1)
        self.assertIsNone(a.above)
        self.assertIsNone(a.below)

    def test_moving_attached_node(self):
        a, b, c = self.sample_node(1), self.sample_node(2), self.sample_node(3)

        self.set_flow(b, c)
        self.set_flow(a, b)

        self.connect_in_order(a, b, c)

        self.assertEqual(a.above, b)
        self.assertEqual(b.above, c)
        self.assertIsNone(c.above)

        self.assertEqual(c.below, b)
        self.assertEqual(b.below, a)
        self.assertIsNone(a.below)

        a.merge(b)

        self.assertEqual(len(a.inflow), 1)
        self.assertEqual(list(a.inflow)[0], c)

        self.assertEqual(a.above, c)
        self.assertIsNone(c.above)
        self.assertEqual(c.below, a)
        self.assertIsNone(a.below)
