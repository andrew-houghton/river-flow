class LocationGraph:
    def __init__(self, height_map):
        factory = LocationGraphFactory(height_map)
        self.first = factory.first
        self.last = factory.last

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
