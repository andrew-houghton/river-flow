class Node:
    def __init__(self):
        self.inflow = set()  # list of nodes which can flow in to this node
        self.outflow = set()  # list of nodes which can flow out of this node
        # pixels on the original which are represented by this node
        self.original_location = set()
        self.altitude = None
        self.flow = 0.0

    def area(self):
        return len(self.original_location)

    def __str__(self):
        return """Node - location:{} altitude:{}""".format(
            self.original_location, self.altitude)
