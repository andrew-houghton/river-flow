from data_structures.location_graph_builder import LocationGraphBuilder
from typing import List

class LocationGraph:
    def __init__(self, height_map: List[List[float]]):
        builder = LocationGraphBuilder(height_map)
        self.lowest = builder.lowest
        self.highest = builder.highest

    def ascending(self):
        node = self.lowest
        while node != None:
            yield node
            node = node.above

    def descending(self):
        node = self.highest
        while node != None:
            yield node
            node = node.below

    def __len__(self):
        return sum(1 for x in self.ascending())

    def __repr__(self):
        return "\n" + str(list(self.ascending())) + "\n"
