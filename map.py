from node import Node


def map_with_index(func, data):
    return [[func(i, j, item) for j, item in enumerate(row)] for i, row in enumerate(data)]


class LocationGraph:
    def __init__(self, height_map):
        self.node_grid = map_with_index(self.to_node, height_map)
        self.connect_nodes()
        make_sorted_linked_list(self.node_grid)

    def to_node(self, row, col, altitude):
        node = Node()
        node.altitude = altitude
        node.original_location.add((row, col))
        return node

    def make_sorted_linked_list(list_of_lists):
        sorted_list = sorted(sum(list_of_lists, []))
        self.highest_node = sorted_list[0]
        self.lowest_node = sorted_list[-1]

        for i in range(len(sorted_list)):
            if i > 0:
                sorted_list[i].prev = sorted_list[i-1]
            if i < len(sorted_list)-1:
                sorted_list[i].next = node[i+1]

    def add_downstream_flow(self, higher_node, lower_node):
        higher_node.outflow.add(lower_node)
        lower_node.inflow.add(higher_node)

    def add_neighbour(self, node, neighbour):
        if node.altitude > neighbour.altitude:
            self.add_downstream_flow(node, neighbour)
        else:
            self.add_downstream_flow(neighbour, node)

    def connect_node(self, row, col, item):
        adjacent_coordinates = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

        for row, col in adjacent_coordinates:
            if 0 <= row < len(self.node_grid) and 0 <= col < len(self.node_grid[0]):
                self.add_neighbour(item, self.node_grid[row][col])
            else:
                item.border == True

    def connect_nodes(self):
        map_with_index(self.connect_node, self.node_grid)
