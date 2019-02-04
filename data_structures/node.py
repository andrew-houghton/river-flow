from operator import attrgetter


def remove_if_exists(_set, item):
    if item in _set:
        _set.remove(item)


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

    def move_flows(self, other, flow, opposite_flow):
        remove_if_exists(flow(other), self)
        for n in flow(other):
            opposite_flow(n).remove(other)
            opposite_flow(n).add(self)
        flow(self).update(flow(other))
        remove_if_exists(flow(self), other)

    def remove(self):
        self.next.prev = self.prev if self.prev is not None else None
        self.prev.next = self.next if self.next is not None else None

    def merge(self, other):
        self.move_flows(other, attrgetter('inflow'), attrgetter('outflow'))
        self.move_flows(other, attrgetter('outflow'), attrgetter('inflow'))

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
