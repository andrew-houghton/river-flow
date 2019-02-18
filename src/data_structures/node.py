from __future__ import annotations
from data_structures.linkset import LinkSet
from typing import Set

class Node:
    def __init__(self):
        self.position: Set[tuple] = set()
        self.home: tuple = None
        self.links: LinkSet = LinkSet(self)
        self.altitude: float = None
        self.flow: float = 0.0
        self.is_border: bool = False
        self.above: Node = None
        self.below: Node = None

    def area(self) -> int:
        return len(self.position)

    def merge(self, other: Node):
        # Disconnect the node we are merging in
        self.links.disconnect(other)
        # Tell the node we are merging in to move it's flow to this node
        other.links.move_all_connections_to(self)
        # Unlink the other node from the linked list
        other._remove()

        self.position.update(other.position)
        self.is_border = self.is_border or other.is_border

        # Pick lower home location
        # self.home = Node._lower_home_location(self.home, other.home)

    # @staticmethod
    # def _lower_home_location(a: tuple, b: tuple) -> tuple:
    #     # return tuple with lowest index, by first index then second
    #     if a[0] > b[0]:
    #         return b
    #     elif a[0] == b[0] and a[1]>b[1]:
    #         return b
    #     else:
    #         return a

    def _remove(self):
        if self.below is None:
            if self.above is None:
                pass
            else:
                self.above.below = None
        else:
            if self.above is None:
                self.below.above = None
            else:
                self.above.below = self.below
                self.below.above = self.above

    def __str__(self):
        return """Node - home:{} altitude:{}""".format(self.home, self.altitude)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.home)

    def __eq__(self, other: Node):
        return other is not None and self.home == other.home
