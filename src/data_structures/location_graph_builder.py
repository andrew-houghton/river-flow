import collections
from operator import attrgetter
from typing import List
from typing import Set
from data_structures.node import Node
from tqdm import tqdm_notebook as tqdm


def map_with_index(func, data, desc=None, progress_bar=False):
    if progress_bar:
        it = enumerate(tqdm(data, desc=desc, unit="nodes", miniters=1))
    else:
        it = enumerate(data)

    return [[func(i, j, item) for j, item in enumerate(row)] for i, row in it]


class LocationGraphBuilder:
    highest: Node
    lowest: Node

    def __init__(self, height_map: List[List[float]]):
        self.node_grid = map_with_index(self.to_node, height_map, "Creating nodes")
        map_with_index(self.set_border, self.node_grid, "Setting border")
        map_with_index(self.connect_node, self.node_grid, "Connecting nodes")
        self.make_sorted_linked_list(self.node_grid)

    def to_node(self, row: int, col: int, altitude: float):
        node = Node()
        node.altitude = altitude
        node.home = (row, col)
        return node

    def set_border(self, i: int, j: int, node: Node):
        node.border = i == 0 or j == 0 or i == len(
            self.node_grid) - 1 or j == len(self.node_grid[0]) - 1

    def connect_node(self, row: int, col: int, item: Node):
        adjacent_coordinates = [(row + 1, col), (row, col + 1)]

        for row, col in adjacent_coordinates:
            if 0 <= row < len(self.node_grid) and 0 <= col < len(self.node_grid[0]):
                neighbour = self.node_grid[row][col]
                
                # used for bfs node merging
                neighbour.touches.append(item)
                item.touches.append(neighbour)

                # used for flow simulation
                if neighbour.altitude < item.altitude:
                    item.outflow.append(neighbour)
                elif neighbour.altitude > item.altitude:
                    neighbour.outflow.append(item)

    def make_sorted_linked_list(self, list_of_lists: List[List[Node]]):
        print("Sorting nodes")
        sorted_list = sorted(sum(list_of_lists, []), key=attrgetter('altitude'))

        self.lowest = sorted_list[0]
        self.highest = sorted_list[-1]

        print("Building linked list")
        for i in range(len(sorted_list)):
            if i > 0:
                sorted_list[i].below = sorted_list[i - 1]
            if i < len(sorted_list) - 1:
                sorted_list[i].above = sorted_list[i + 1]