
def add_location_to_list(data):


def to_node(row, col, altitude):
    node = Node()
    node.altitude = altitude
    node.original_location.add((row, col))
    return node


def create_nodes(height_map):
    return [[to_node(i, j, height_reading) for j, height_reading in enumerate(row)]
        for i, row in enumerate(height_map)]


def within_array_bounds(array, index):
    if index[0] < 0 or index[1] < 0:
        return False
    if index[0] >= len(array):
        return False
    if index[1] >= len(array[0]):
        return False
    return True


def connect_node(nodes, row, col):
    adjacent_coordinates = [
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1)]
    neighbours = [nodes[coord[0]][coord[1]]
                  for coord in adjacent_coordinates if within_array_bounds(nodes, coord)]

    for neighbour in neighbours:
        add_neighbour(nodes[row][col], neighbour)
    nodes[row][col].border = len(neighbours) != 4


def connect_nodes(nodes):
    for row in range(len(nodes)):
        for col in range(len(nodes[row])):
            connect_node(nodes, row, col)




class LocationGraph:
    def __init__(self, height_map):
        self.node_grid = create_nodes(height_grid)
        self.connect_nodes()
    
    def connect_nodes():
