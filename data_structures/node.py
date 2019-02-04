from operator import attrgetter


class Node:
    def __init__(self):
        self.inflow = set()  # list of nodes which can flow in to this node
        self.outflow = set()  # list of nodes which can flow out of this node
        self.original_location = set()
        self.altitude = None
        self.flow = 0.0
        self.border = False
        self.next = None
        self.prev = None
        self._iteration_index = None

    def area(self):
        return len(self.original_location)

    def move_flows(self, other):
        # for each node with a flow connected to other
        # change flow other -> self

        # put flows that belong in self

        # make sure other is not in flows
        pass

    def remove(self):
        pass

    def merge(self, other):
        self.move_flows(other)

        self.original_location.update(other.original_location)
        self.border = self.border or other.border
  
        other.remove()

    def __str__(self):
        return """Node - location:{} altitude:{}""".format(
            self.original_location, self.altitude)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(tuple(self.original_location))
