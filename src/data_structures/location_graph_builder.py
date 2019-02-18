from operator import attrgetter

from data_structures.node import Node


def map_with_index(func, data):
    return [[func(i, j, item) for j, item in enumerate(row)] for i, row in enumerate(data)]


class LocationGraphBuilder:
    def __init__(self, height_map):
        self.node_grid = map_with_index(self.to_node, height_map)
        map_with_index(self.set_border, self.node_grid)
        self.connect_nodes()
        self.make_sorted_linked_list(self.node_grid)
        self.merge_equal_height_nodes()

    def to_node(self, row, col, altitude):
        node = Node()
        coordinates = (row, col)

        node.altitude = altitude
        node.original_location.add(coordinates)
        node.starting_location = coordinates
        return node

    def set_border(self, i, j, node):
        node.border = i == 0 or j == 0 or i == len(
            self.node_grid) - 1 or j == len(self.node_grid[0]) - 1

    def connect_nodes(self):
        map_with_index(self.connect_node, self.node_grid)

    def connect_node(self, row, col, item):
        adjacent_coordinates = [(row + 1, col), (row, col + 1)]

        for row, col in adjacent_coordinates:
            if 0 <= row < len(self.node_grid) and 0 <= col < len(self.node_grid[0]):
                self.add_neighbour(item, self.node_grid[row][col])

    def add_neighbour(self, node, neighbour):
        if node.altitude > neighbour.altitude:
            self.add_downstream_flow(node, neighbour)
        else:
            self.add_downstream_flow(neighbour, node)

    def add_downstream_flow(self, higher_node, lower_node):
        higher_node.outflow.add(lower_node)
        lower_node.inflow.add(higher_node)

    def make_sorted_linked_list(self, list_of_lists):
        sorted_list = sorted(sum(list_of_lists, []),
                             key=attrgetter('altitude'))
        self.first = sorted_list[0]  # Lowest node
        self.last = sorted_list[-1]  # Highest node

        for i in range(len(sorted_list)):
            if i > 0:
                sorted_list[i].prev = sorted_list[i - 1]
            if i < len(sorted_list) - 1:
                sorted_list[i].next = sorted_list[i + 1]

    def print_array(self, blank):
        print(' '.join(str(i) for i in blank[0:3]))
        print(' '.join(str(i) for i in blank[3:6]))
        print(' '.join(str(i) for i in blank[6:9]))

    def print_state(self):
        blank = [0]*9

        for i in self.ascending():
            for j in i.original_location:
                blank[Node.num(j)-1] = Node.num(i.starting_location)
        self.print_array(blank)

        last_node_neighbours = [str(Node.num(i.starting_location)) for i in self.last.inflow.union(self.last.outflow)]
        print(f'Last node neighbours {",".join(last_node_neighbours)}')

    def merge_equal_height_nodes(self):
        print('Initial state')
        self.print_state()
        for node in self.ascending():
            print(f'Working on node {Node.num(node.starting_location)}')
            for neighbour in node.inflow.union(node.outflow):
                if neighbour.altitude == node.altitude:
                    node.merge(neighbour)
            self.print_state()

    def ascending(self):
        node = self.first
        while node != None:
            yield node
            node = node.next
