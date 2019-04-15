from queue import PriorityQueue


def generate_lake(point):
    # Store points which are part of the lake in a list
    lake = []

    # Store points which are yet to be visited in a priority queue (which represents the border of the lake)
    border = PriorityQueue()
    border.put(point)

    # Store the altitude of the lake
    lake_altitude = point.altitude

    # Should not need this while condition but whatever
    while not border.empty():
        item = border.get()

        # Exit if this point is the outflow point for the lake
        if item.altitude >= lake_altitude:
            # Update lake altitude
            lake_altitude = item.altitude
            # Include this point in the lake
            lake.append(item)
            # Add all this points neighbours to the lake border
            for neighbour in item.inflow:  
                border.put(neighbour)
        else:
            break

    # TODO will border contain any points which are the same height as the lake?
    # This is possible and they should be added to the lake.

    return (item, lake)

