
class Node:
    def __init__(self):
        self.inflow = set()  # list of nodes which can flow in to this node
        self.outflow = set()  # list of nodes which can flow out of this node
        self.original_location = set()
        self.starting_location = None
        self.altitude = None
        self.flow = 0.0
        self.border = False
        self.next = None
        self.prev = None
        self._iteration_index = None

    @staticmethod
    def num(location):
        return location[0] * 3 + location[1]

    def area(self):
        return len(self.original_location)

    def move_connections_to(self, node):
        for i in self.inflow:
            # print(f'\t\tdisconnecting {self.num(i.starting_location)} from {self.num(self.starting_location)}')
            i.remove_outflow(self)
            i.outflow.add(node)

        for i in self.outflow:
            # print(f'\t\tdisconnecting {self.num(i.starting_location)} from {self.num(self.starting_location)}')
            i.remove_inflow(self)
            i.inflow.add(node)

        # Verify node is disconnected
        for i in self.inflow:
            if self in i.outflow:
                # print(f'\tError: {self.num(i.starting_location)} is still connected to {self.num(self.starting_location)}')
                assert False
        for i in self.outflow:
            if self in i.inflow:
                # print(f'\tError: {self.num(i.starting_location)} is still connected to {self.num(self.starting_location)}')
                assert False

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
        print(f"      Merging {self.num(other.starting_location)} into {self.num(self.starting_location)}")

        self.move_flows(other)

        self.original_location.update(other.original_location)
        self.border = self.border or other.border

        if other.starting_location[0] < self.starting_location[0]:
            self.starting_location = other.starting_location
        elif other.starting_location[0] == self.starting_location[0] and \
                other.starting_location[1] < self.starting_location[1]:
            # Keep the lower index item
            self.starting_location = other.starting_location

        print(f"       {self.num(self.starting_location)} now has {','.join(str(self.num(i)) for i in self.original_location)}")

    def __str__(self):
        return """Node - location:{} altitude:{}""".format(
            self.original_location, self.altitude)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.starting_location)

    def __eq__(self, other):
        return other is not None and self.starting_location == other.starting_location
