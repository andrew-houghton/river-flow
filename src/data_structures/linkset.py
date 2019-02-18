from __future__ import annotations
from typing import Set
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from data_structures.node import Node

class LinkSet:
    def __init__(self, node: Node):
        self.node: Node = node
        self._items: Set[Node] = set()

    def link(self, other: Node):
        # create a link to another node
        self._add(other)
        other.links._add(self.node)

    def _move_connection_to(self, origin: Node, destination: Node):
        # origin node can't connect anymore
        self.disconnect(origin)
        # destination must get the connection
        self.link(destination)

    def move_all_connections_to(self, other: Node):
        for n in self.all():
            n.links._move_connection_to(self.node,other)

    def disconnect(self, other: Node):
        # disconnect this from other
        self._remove(other)
        other.links._remove(self.node)

    def all(self) -> Set[Node]:
        return self._items

    def inflow(self) -> Set[Node]:
        for i in self.all():
            if i.altitude > self.node.altitude:
                yield i

    def outflow(self) -> Set[Node]:
        for i in self.all():
            if i.altitude < self.node.altitude:
                yield i

    def _remove(self, other: Node):
        self._items.remove(other)

    def _add(self, node: Node):
        self._items.add(node)
