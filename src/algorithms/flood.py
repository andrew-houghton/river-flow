from sortedcontainers import SortedKeyList
from data_structures.node import Node
from typing import Iterable


def start_flood(lake: Node):
    # add neighbours to sorted collection
    edge_of_lake = SortedKeyList(key=lambda node: node.altitude)
    edge_of_lake.update(lake.links.inflow())

    # Once we look at an item we are done with it
    next_lowest_neighbour = edge_of_lake.pop()

    while next_lowest_neighbour.altitude > lake.altitude and not lake.border:
        # merge node into next lowest neighbour
        next_lowest_neighbour.merge(lake)

        # move to look at next node on the edge of the flood
        lake = next_lowest_neighbour
        try:
            next_lowest_neighbour = edge_of_lake.pop()
        except IndexError as e:
            raise IndexError("No nodes left on the edge of the lake to add but flooding not complete.") from e


def flood(nodes: Iterable[Node]):
    # from lowest altitude to highest find the low points and flood them
    for node in nodes:
        if len(list(node.links.outflow())) == 0 and \
                not node.is_border and \
                len(list(node.links.inflow())) > 0:
            start_flood(node)
