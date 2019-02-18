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

    def merge(self, other: Node):
        other._remove()

    def __str__(self):
        return """Node - home:{} altitude:{}""".format(self.home, self.altitude)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.home)

    def __eq__(self, other: Node):
        return other is not None and self.home == other.home
