from tqdm import tqdm_notebook as tqdm


def flow(graph, image_writer, size):
    print("Running flow simulation")
    for node in tqdm(graph.descending(), total=size[0]*size[1], unit=" nodes"):
        node.flow += node.area()
        if node.links.len_outflow() > 0 and not node.border:
            total_height_out = 0.0
            for i in node.links.outflow():
                total_height_out += node.altitude - i.altitude

            for i in node.links.outflow():
                i.flow += (node.altitude - i.altitude) * node.flow / total_height_out
        image_writer.update(node)
    return graph
