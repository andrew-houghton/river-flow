from data_structures.location_graph import LocationGraph


def flow(graph: LocationGraph, image_writer):
    for node in graph.descending():
        node.flow += node.area()
        if node.links.len_outflow() > 0 and not node.border:
            total_height_out = 0.0
            for i in node.links.outflow():
                total_height_out += node.altitude - i.altitude

            for i in node.links.outflow():
                i.flow += (node.altitude - i.altitude) * node.flow / total_height_out
        image_writer.update(node)
    return graph
