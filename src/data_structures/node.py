from __future__ import annotations

from typing import Set

from data_structures.linkset import LinkSet


class Node:
    def __init__(self):
        self.home: tuple = None
        self.links: LinkSet = LinkSet(self)
        self.altitude: float = None
        self.flow: float = 0.0
        self.is_border: bool = False
        self.above: Node = None
        self.below: Node = None

    def area(self) -> int:
        return 1

    def __str__(self):
        return """Node - home:{} altitude:{}""".format(self.home, self.altitude)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.home)

    def __eq__(self, other: Node):
        return other is not None and self.home == other.home
