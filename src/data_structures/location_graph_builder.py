import collections
from operator import attrgetter
from typing import List
from typing import Set
from data_structures.node import Node
from tqdm import tqdm


def map_with_index(func, data, desc=None, progress_bar=True):
    if progress_bar:
        it = enumerate(tqdm(data, desc=desc, unit="nodes", miniters=1))
    else:
        it = enumerate(data)

    return [[func(i, j, item) for j, item in enumerate(row)] for i, row in it]

def overlaps(a, b):
    return len(a.intersection(b)) > 0


class LocationGraphBuilder:
    highest: Node
    lowest: Node

    def __init__(self, height_map: List[List[float]]):
        print("Creating graph")
        self.node_grid = map_with_index(self.to_node, height_map, "Creating nodes")
        map_with_index(self.set_border, self.node_grid, "Setting border")
        map_with_index(self.connect_node, self.node_grid, "Connecting nodes")
        self.merge_equal_height_nodes(self.node_grid)
        nodes = self.make_clean_node_list(self.node_grid)
        self.make_sorted_linked_list(nodes)

    def to_node(self, row: int, col: int, altitude: float):
        node = Node()
        node.altitude = altitude
        node.position = {(row, col)}
        node.deleted = False
        return node

    def set_border(self, i: int, j: int, node: Node):
        node.is_border = i == 0 or j == 0 or i == len(
            self.node_grid) - 1 or j == len(self.node_grid[0]) - 1

    def connect_node(self, row: int, col: int, item: Node):
        adjacent_coordinates = [
            (row + 1, col),
            (row, col + 1),
            (row + 1, col - 1),
            (row + 1, col + 1)
        ]

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

    def find_attached_equal_height_nodes(self, node: Node) -> Set[Node]:
        # Breadth first search
        seen, queue = {node}, collections.deque([node])
        while queue:
            vertex = queue.popleft()
            equal_height_neighbours = [i for i in vertex.touches if i.altitude == vertex.altitude]
            for neighbour in equal_height_neighbours:
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        return seen

    def merge_node_set_into_node(self, original: Node, attached: Set[Node]):
        # border attribute should be true if any are borders
        original.is_border = any([i.is_border for i in attached])

        # all nodes in attached should be removed from grid
        for i in attached:
            if i.position != original.position:
                i.deleted = True

        # position should cover all attached
        original.position = set.union(*[i.position for i in attached])

        # final outflow is the outflow for all nodes except outflows to itself
        all_possible_outflows = []
        for i in attached:
            for j in i.outflow:
                if not overlaps(j.position, original.position):
                    if not any([overlaps(j.position, k.position) for k in all_possible_outflows]):
                        all_possible_outflows.append(j)

        original.outflow = all_possible_outflows


    def merge_equal_height_nodes(self, node_grid):
        print("Merging equal height nodes")
        # TODO tqdm this loop
        for row in node_grid:
            for node in row:
                if not node.deleted:
                    num_equal_height_neighbours = len([i for i in node.touches if i.altitude == node.altitude])
                    if num_equal_height_neighbours > 0:
                        attached_nodes = self.find_attached_equal_height_nodes(node)
                        self.merge_node_set_into_node(node, attached_nodes)

    def make_clean_node_list(self, node_grid):
        print('Creating clean node list')
        nodes = [i for i in sum(node_grid, []) if not i.deleted]

        for node in nodes:
            for i in node.outflow:
                if i.deleted:
                    node.outflow.remove(i)

        for node in nodes:
            del node.deleted
            del node.touches

        return nodes

    def make_sorted_linked_list(self, nodes: List[Node]):
        print("Sorting nodes")
        sorted_list = sorted(nodes, key=attrgetter('altitude'))

        self.lowest = sorted_list[0]
        self.highest = sorted_list[-1]

        # print("Building linked list")
        for i in range(len(sorted_list)):
            if i > 0:
                sorted_list[i].below = sorted_list[i - 1]
            if i < len(sorted_list) - 1:
                sorted_list[i].above = sorted_list[i + 1]
