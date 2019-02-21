from operator import attrgetter
import collections

from data_structures.node import Node
from typing import List
from typing import Set

def map_with_index(func, data):
    return [[func(i, j, item) for j, item in enumerate(row)] for i, row in enumerate(data)]


class LocationGraphBuilder:
    def __init__(self, height_map: List[List[float]]):
        self.node_grid = map_with_index(self.to_node, height_map)
        map_with_index(self.set_border, self.node_grid)
        map_with_index(self.connect_node, self.node_grid)
        self.make_sorted_linked_list(self.node_grid)
        self.merge_equal_height_nodes()

    def to_node(self, row: int, col: int, altitude: float):
        node = Node()
        coordinates = (row, col)
        node.altitude = altitude
        node.position.add(coordinates)
        node.home = coordinates
        return node

    def set_border(self, i: int, j: int, node: Node):
        node.border = i == 0 or j == 0 or i == len(
            self.node_grid) - 1 or j == len(self.node_grid[0]) - 1

    def connect_node(self, row: int, col: int, item: Node):
        adjacent_coordinates = [(row + 1, col), (row, col + 1)]

        for row, col in adjacent_coordinates:
            if 0 <= row < len(self.node_grid) and 0 <= col < len(self.node_grid[0]):
                neighbour = self.node_grid[row][col]
                item.links.link(neighbour)

    def make_sorted_linked_list(self, list_of_lists: List[List[Node]]):
        sorted_list = sorted(sum(list_of_lists, []), key=attrgetter('altitude'))

        self.lowest = sorted_list[0]
        self.highest = sorted_list[-1]

        for i in range(len(sorted_list)):
            if i > 0:
                sorted_list[i].below = sorted_list[i - 1]
            if i < len(sorted_list) - 1:
                sorted_list[i].above = sorted_list[i + 1]

    def bfs(self, node: Node) -> Set[Node]:
        seen, queue = {node}, collections.deque([node])
        while queue:
            vertex = queue.popleft()
            for neighbour in vertex.links.equal_height():
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        return seen

    def merge(self, original: Node, attached: Set[Node]):
        for n in attached:
            n.remove()
            original.is_border = original.is_border or n.is_border
            original.position.update(n.position)
            original.links.update(n.links)
        original.links.disconnect_all(attached)

    def merge_equal_height_nodes(self):
        # TODO check that ascending isn't keeping reference to nodes which are gone
        for node in self.ascending():
            self.merge(node, self.bfs(node))

    def ascending(self):
        node = self.lowest
        while node != None:
            yield node
            node = node.above
