from __future__ import annotations

from typing import Set

class Node:
    def __init__(self):
        self.touches = []
        self.outflow = []
        self.altitude: float = None
        self.flow: float = 0.0
        self.is_border: bool = False
        self.above: Node = None
        self.below: Node = None
        self.position: set = None

    def area(self) -> int:
        return len(self.position)

    def __str__(self):
        return """Node - position:{} altitude:{}""".format(self.position, self.altitude)

    def __repr__(self):
        return self.__str__()
