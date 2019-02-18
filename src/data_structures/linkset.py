from data_structures.node import Node

class LinkSet:
    def __init__(self, node: Node):
        self.node = node

    def link(self, other: Node):
        # store a link to another node
        pass

    def move_flow(self, other: Node):
        # move all the connections in this LinkSet to connect to other instead
        pass

    def remove(self, other: Node):
        # disconnect this from other
        pass

