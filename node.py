class Node:
    def __init__(self):
        self.inflow = set()  # list of nodes which can flow in to this node
        self.outflow = set()  # list of nodes which can flow out of this node
        self.original_location = set()
        self.altitude = None
        self.flow = 0.0
        self.border = False
        self.next=None
        self.prev=None
        self._iteration_index=None

    def area(self):
        return len(self.original_location)

    def __str__(self):
        return """Node - location:{} altitude:{}""".format(
            self.original_location, self.altitude)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(tuple(self.original_location))