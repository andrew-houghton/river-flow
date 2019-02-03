def simulate_flow(graph, image_writer):
    for node in graph.descending():
        node.flow += node.area()
        if len(node.outflow) > 0 and not node.border:
            total_height_out = 0.0
            for i in node.outflow:
                total_height_out += node.altitude-i.altitude

            for i in node.outflow:
                i.flow += (node.altitude-i.altitude)*node.flow/total_height_out
        image_writer.write(graph)
    return graph