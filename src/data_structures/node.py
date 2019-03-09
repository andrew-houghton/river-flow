from __future__ import annotations

from typing import Set

class Node:
    def __init__(self):
        self.home: tuple = None
        self.touches = []
        self.outflow = []
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
