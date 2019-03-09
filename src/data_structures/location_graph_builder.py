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
        # print("Creating graph")
        self.node_grid = map_with_index(self.to_node, height_map, "Creating nodes")
        map_with_index(self.set_border, self.node_grid, "Setting border")
        map_with_index(self.connect_node, self.node_grid, "Connecting nodes")
        self.merge_equal_height_nodes(self.node_grid)
        nodes = self.make_clean_node_list(self.node_grid)
        self.make_sorted_linked_list(nodes)

    def to_node(self, row: int, col: int, altitude: float):
        node = Node()
        node.altitude = altitude
        node.home = (row, col)
        node.position = {(row, col)}
        node.deleted = False
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

    def bfs(self, node: Node) -> Set[Node]:
        seen, queue = {node}, collections.deque([node])
        while queue:
            vertex = queue.popleft()
            equal_height_neighbours = [i for i in vertex.touches if i.altitude == vertex.altitude]
            for neighbour in equal_height_neighbours:
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        return seen

    def merge(self, original: Node, attached: Set[Node]):
        # border attribute shuold be on if any are borders
        original.is_border = any([i.is_border for i in attached])

        # position should cover all attached
        original.position = set([i.home for i in attached])

        # final outflow is the outflow for all nodes except outflows to itself
        all_possible_outflows = []
        for i in attached:
            all_possible_outflows += [j for j in i.outflow if j.home not in original.position]
        original.outflow = all_possible_outflows

        # all nodes in attached should be removed from grid
        for i in attached:
            if i.home != original.home:
                i.deleted = True

    def merge_equal_height_nodes(self, node_grid):
        # print("Merging equal height nodes")
        # TODO tqdm this loop
        for row in node_grid:
            for node in row:
                if not node.deleted:
                    if len([i for i in node.touches if i.altitude == node.altitude]) > 0:
                        attached_nodes = self.bfs(node)
                        self.merge(node, attached_nodes)

    def make_clean_node_list(self, node_grid):
        nodes = [i for i in sum(node_grid, []) if not i.deleted]
        for node in nodes:
            del node.deleted
            del node.touches
        return nodes

    def make_sorted_linked_list(self, nodes: List[Node]):
        # print("Sorting nodes")
        sorted_list = sorted(nodes, key=attrgetter('altitude'))

        self.lowest = sorted_list[0]
        self.highest = sorted_list[-1]

        # print("Building linked list")
        for i in range(len(sorted_list)):
            if i > 0:
                sorted_list[i].below = sorted_list[i - 1]
            if i < len(sorted_list) - 1:
                sorted_list[i].above = sorted_list[i + 1]