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

    def move_connections_to(self, node):
        for i in self.inflow:
            i.remove_outflow(self)
            i.outflow.add(node)

        for i in self.outflow:
            i.remove_inflow(self)
            i.inflow.add(node)

    def remove_inflow(self, item):
        if item in self.inflow:
            self.inflow.remove(item)

    def remove_outflow(self, item):
        if item in self.outflow:
            self.outflow.remove(item)

    def move_flows(self, other):
        other.remove_inflow(self)
        other.remove_outflow(self)
        self.remove_outflow(other)
        self.remove_inflow(other)

        other.move_connections_to(self)

        self.inflow.update(other.inflow)
        self.outflow.update(other.outflow)

        other.remove()

    def remove(self):
        print('remove')
        if self.prev is None:
            if self.next is None:
                print('wat')
            else:
                self.next.prev = None
        else:
            if self.next is None:
                self.prev.next = None
            else:
                self.next.prev = self.prev
                self.prev.next = self.next


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
