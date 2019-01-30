from sortedcollections import SortedList

def start_flood(nodes, node):
	# add neighbours to sorted collection
	sl = SortedList()
	sl.update(node.inflow)
	next_lowest_neighbour = sl.pop()
	while next_lowest_neighbour.altitude>node.altitude:
		# merge node into next lowest neighbour
		next_lowest_neighbour=sl.pop()
		break 

def flood(nodes):
	# from lowest altitude to highest find the low points and flood them
	for node in nodes:
		if len(node.outflow)==0 and not node.border:
			print("low point found")
			start_flood(nodes, node)
