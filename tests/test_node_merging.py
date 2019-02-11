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
        n.starting_location = coordinates
        n.original_location.add(coordinates)
        return n

    @staticmethod
    def connect_in_order(*args):
        for i in range(len(args)-1):
            args[i].next = args[i+1]
            args[i+1].prev = args[i]

    def test_simple_case(self):
        a, b = self.sample_node(1), self.sample_node(2)
        self.set_flow(a, b)

        self.connect_in_order(a, b)

        self.assertEqual(a.next, b)
        self.assertIsNone(b.next)
        self.assertEqual(b.prev, a)
        self.assertIsNone(a.prev)

        a.merge(b)

        self.assertEqual(a.original_location, {(0, 1), (0, 2)})
        self.assertEqual(a.altitude, 1)
        self.assertIsNone(a.next)
        self.assertIsNone(a.prev)

    def test_moving_attached_node(self):
        a, b, c = self.sample_node(1), self.sample_node(2), self.sample_node(3)

        self.set_flow(b, c)
        self.set_flow(a, b)

        self.connect_in_order(a, b, c)

        self.assertEqual(a.next, b)
        self.assertEqual(b.next, c)
        self.assertIsNone(c.next)

        self.assertEqual(c.prev, b)
        self.assertEqual(b.prev, a)
        self.assertIsNone(a.prev)

        a.merge(b)

        self.assertEqual(len(a.inflow), 1)
        self.assertEqual(list(a.inflow)[0], c)

        self.assertEqual(a.next, c)
        self.assertIsNone(c.next)
        self.assertEqual(c.prev, a)
        self.assertIsNone(a.prev)
