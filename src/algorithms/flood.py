from sortedcollections import SortedList


def start_flood(lake):
    # add neighbours to sorted collection
    edge_of_lake = SortedList()
    edge_of_lake.update(lake.inflow)

    # Once we look at an item we are done with it
    next_lowest_neighbour = edge_of_lake.pop()
    while next_lowest_neighbour.altitude > lake.altitude and not lake.border:
        # merge node into next lowest neighbour
        next_lowest_neighbour.merge(lake)

        # move to look at next node on the edge of the flood
        lake = next_lowest_neighbour
        try:
            next_lowest_neighbour = edge_of_lake.pop()
        except IndexError as e:
            raise IndexError("No nodes left on the edge of the lake to add.") from e


def flood(nodes):
    # from lowest altitude to highest find the low points and flood them
    for node in nodes:
        if len(node.outflow) == 0 and not node.border:
            start_flood(node)