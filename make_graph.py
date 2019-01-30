from node import Node
from operator import attrgetter


def to_node(row, col, altitude):
    node = Node()
    node.altitude = altitude
    node.original_location.add((row, col))
    return node


def add_location_to_list(data):
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = (i, j, data[i][j])
    return data


def map_to_node(data):
    return [[to_node(*item) for item in row] for row in data]


def within_array_bounds(array, index):
    if index[0] < 0 or index[1] < 0:
        return False
    if index[0] >= len(array):
        return False
    if index[1] >= len(array[0]):
        return False
    return True


def add_neighbour(node, neighbour):
    if node.altitude > neighbour.altitude:
        node.outflow.add(neighbour)
        neighbour.inflow.add(node)
    else:
        node.inflow.add(neighbour)
        neighbour.outflow.add(node)


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


def connect_all_nodes(nodes):
    for row in range(len(nodes)):
        for col in range(len(nodes[row])):
            connect_node(nodes, row, col)


def remove_if_exists(full_set, item):
    if item in full_set:
        full_set.remove(item)


def merge_pair(nodes, a, b):
    a.inflow.update(b.inflow)
    a.outflow.update(b.outflow)
    remove_if_exists(a.inflow, a)
    remove_if_exists(a.inflow, b)
    remove_if_exists(a.outflow, a)
    remove_if_exists(a.outflow, b)
    a.border = a.border or b.border
    b.deleted = True
    a.original_location.update(b.original_location)


def merge_equal_height_nodes(nodes):
    # Find equal height nodes
    for node in nodes:
        if not node.deleted:
            # Check all neighbours of the nodes
            for neighbour in node.inflow.union(node.outflow):
                if neighbour.altitude == node.altitude:
                    merge_pair(nodes, node, neighbour)
    # Discard deleted nodes
    return [i for i in nodes if not i.deleted]


def convert_to_graph(data):
    location_and_altitude = add_location_to_list(data)
    nodes = map_to_node(location_and_altitude)
    connect_all_nodes(nodes)
    node_list = sum(nodes, [])
    node_list = merge_equal_height_nodes(node_list)
    return sorted(node_list, key=attrgetter('altitude'))
