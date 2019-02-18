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

    def move_flow(self, other: Node):
        # move all the connections in this LinkSet to connect to other instead
        pass

    def disconnect(self, other: Node):
        # disconnect this from other
        self._remove(other)
        other.links._remove(self.node)

    def all(self) -> Set[Node]:
        return self._items

    def _remove(self, other: Node):
        self._items.remove(other)

    def _add(self, node: Node):
        self._items.add(node)
