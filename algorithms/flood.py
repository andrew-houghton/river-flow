from sortedcollections import SortedList

def start_flood(lake):
    # add neighbours to sorted collection
    edge_of_flood = SortedList()
    edge_of_flood.update(lake.inflow)

    next_lowest_neighbour = edge_of_flood.pop() # Once we look at an item we are done with it
    while next_lowest_neighbour.altitude > lake.altitude and not lake.border:
        # merge node into next lowest neighbour
        next_lowest_neighbour.merge(lake)

        # move to look at next node on the edge of the flood
        lake = next_lowest_neighbour
        next_lowest_neighbour = edge_of_flood.pop()


def flood(nodes):
    # from lowest altitude to highest find the low points and flood them
    for node in nodes:
        if len(node.outflow) == 0 and not node.border:
            print("low point found")
            start_flood(node)
