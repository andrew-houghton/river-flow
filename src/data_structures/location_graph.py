from data_structures.location_graph_builder import LocationGraphBuilder


class LocationGraph:
    def __init__(self, height_map):
        builder = LocationGraphBuilder(height_map)
        self.first = builder.first
        self.last = builder.last

    def ascending(self):
        node = self.first
        while node != None:
            yield node
            node = node.next

    def descending(self):
        node = self.last
        while node != None:
            yield node
            node = node.prev

    def length(self):
        return sum(1 for x in self.ascending())

    def __repr__(self):
        return "\n" + str(list(self.ascending())) + "\n"
