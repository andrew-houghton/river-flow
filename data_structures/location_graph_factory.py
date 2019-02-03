from node import Node
from operator import attrgetter


class LocationGraphFactory:
    def __init__(self, height_map):
        self.node_grid = self.map_with_index(self.to_node, height_map)
        self.map_with_index(self.set_border, self.node_grid)
        self.connect_nodes()
        self.make_sorted_linked_list(self.node_grid)
        self.merge_equal_height_nodes()

    def set_border(self, i, j, node):
        node.border = i == 0 or j == 0 or i == len(
            self.node_grid)-1 or j == len(self.node_grid[0])-1

    def map_with_index(self, func, data):
        return [[func(i, j, item) for j, item in enumerate(row)] for i, row in enumerate(data)]

    def to_node(self, row, col, altitude):
        node = Node()
        node.altitude = altitude
        node.original_location.add((row, col))
        return node

    def make_sorted_linked_list(self, list_of_lists):
        sorted_list = sorted(sum(list_of_lists, []),
                             key=attrgetter('altitude'))
        self.first = sorted_list[0]  # Lowest node
        self.last = sorted_list[-1]  # Highest node

        for i in range(len(sorted_list)):
            if i > 0:
                sorted_list[i].prev = sorted_list[i-1]
            if i < len(sorted_list)-1:
                sorted_list[i].next = sorted_list[i+1]

    def add_downstream_flow(self, higher_node, lower_node):
        higher_node.outflow.add(lower_node)
        lower_node.inflow.add(higher_node)

    def add_neighbour(self, node, neighbour):
        if node.altitude > neighbour.altitude:
            self.add_downstream_flow(node, neighbour)
        else:
            self.add_downstream_flow(neighbour, node)

    def connect_node(self, row, col, item):
        adjacent_coordinates = [
            (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

        for row, col in adjacent_coordinates:
            if 0 <= row < len(self.node_grid) and 0 <= col < len(self.node_grid[0]):
                self.add_neighbour(item, self.node_grid[row][col])

    def connect_nodes(self):
        self.map_with_index(self.connect_node, self.node_grid)

    def remove_if_exists(self, full_set, item):
        if item in full_set:
            full_set.remove(item)

    def join_flow_sets(self, a, b):
        a.inflow.update(b.inflow)
        a.outflow.update(b.outflow)
        self.remove_if_exists(a.inflow, a)
        self.remove_if_exists(a.inflow, b)
        self.remove_if_exists(a.outflow, a)
        self.remove_if_exists(a.outflow, b)

    def remove_node(self, node):
        if node.next is not None:
            node.next.prev = node.prev
        if node.prev is not None:
            node.prev.next = node.next

    def merge_pair(self, original_node, merged_node):
        self.join_flow_sets(original_node, merged_node)
        original_node.border = original_node.border or merged_node.border
        original_node.original_location.update(merged_node.original_location)
        self.remove_node(merged_node)

    def merge_equal_height_nodes(self):
        for node in self.ascending():
            for neighbour in node.inflow.union(node.outflow):
                if neighbour.altitude == node.altitude:
                    self.merge_pair(node, neighbour)

    def ascending(self):
        node = self.first
        while node != None:
            yield node
            node = node.next

    def descending(self):
        node = self.last
        while node != None:
            yield node
            node = node.prev

    def length(self):
        return sum(1 for x in self.ascending())
