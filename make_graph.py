from node import Node
from operator import attrgetter


def to_node(row, col, altitude):
    node = Node()
    node.altitude = altitude
    node.original_location.add((row, col))
    return node


def map_to_node(data):
    for row in range(len(data)):
        for col in range(len(data[row])):
            data[row][col] = to_node(row, col, data[row][col])
    return data


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


def connect_all_nodes(nodes):
    for row in range(len(nodes)):
        for col in range(len(nodes[row])):
            connect_node(nodes, row, col)


def convert_to_graph(data):
    nodes = map_to_node(data)
    connect_all_nodes(nodes)
    node_list = sum(nodes, [])
    return sorted(node_list, key=attrgetter('altitude'))
