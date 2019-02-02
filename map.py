from node import Node


def map_with_index(func, data):
    return [[func(i, j, item) for j, item in enumerate(row)] for i, row in enumerate(data)]


def flatten_list(list_of_lists):
    return sum(list_of_lists, [])


class LocationGraph:
    def to_node(self, row, col, altitude):
        node = Node()
        node.altitude = altitude
        node.original_location.add((row, col))
        return node

    def __init__(self, height_map):
        self.node_grid = map_with_index(self.to_node, height_map)
        self.connect_nodes()
        self.node_list = flatten_list(self.node_grid)

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
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1)
        ]

        for row, col in adjacent_coordinates:
            if 0 <= row < len(self.node_grid) and 0 <= col < len(self.node_grid[0]):
                self.add_neighbour(item, self.node_grid[row][col])
            else:
                item.border == True

    def connect_nodes(self):
        map_with_index(self.connect_node, self.node_grid)
