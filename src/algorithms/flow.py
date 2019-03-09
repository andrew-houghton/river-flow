from tqdm import tqdm_notebook as tqdm


def flow(graph, image_writer, size=(0,0), progress_bar=False):
    print("Running flow simulation")
    if progress_bar:
        it = tqdm(graph.descending(), total=size[0]*size[1], unit=" nodes")
    else:
        it = graph.descending()

    for node in it:
        node.flow += node.area()
        if len(node.outflow) > 0 and not node.border:
            total_height_out = 0.0
            for i in node.outflow:
                total_height_out += node.altitude - i.altitude

            for i in node.outflow:
                i.flow += (node.altitude - i.altitude) * node.flow / total_height_out
        image_writer.update(node)
    return graph
