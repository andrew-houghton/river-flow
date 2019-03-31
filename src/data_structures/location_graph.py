from typing import List
from data_structures.location_graph_builder import LocationGraphBuilder


class LocationGraph:
    def __init__(self, height_map: List[List[float]], config: dict={}):
        self.height = len(height_map)
        self.width = len(height_map[0])
        builder = LocationGraphBuilder(height_map)
        self.lowest = builder.lowest
        self.highest = builder.highest

        self.config = config

    def ascending(self):
        node = self.lowest
        while node is not None:
            yield node
            node = node.above

    def descending(self):
        node = self.highest
        while node is not None:
            yield node
            node = node.below

    def __len__(self):
        return sum(1 for x in self.ascending())

    def __repr__(self):
        return "\n" + str(list(self.ascending())) + "\n"
