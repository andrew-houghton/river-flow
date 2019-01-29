from node import Node
from operator import attrgetter

def to_node(args):
	row, col, altitude = args
	node = Node()
	node.altitude = altitude
	node.original_location = (row,col)
	return node

def store_location(two_dimensional_list):
	output = []
	for rownum in range(len(two_dimensional_list)):
		for colnum in range(len(two_dimensional_list[rownum])):
			output.append((
				rownum,
				colnum,
				two_dimensional_list[rownum][colnum]
				))
	return output

def convert_to_graph(data):
	all_heights = store_location(data)
	all_nodes = map(to_node, all_heights)

	return sorted(all_nodes, key=attrgetter('altitude'))
