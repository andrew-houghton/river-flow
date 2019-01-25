class Node:
    def __init__(self):
        self.neighbours = [] # list of nodes which can flow in/out to this node
        self.original_location = [] # pixels on the original which are represented by this node
        self.altitude = None
        self.flow = 0.0

    def area(self):
        return len(self.original_location)
