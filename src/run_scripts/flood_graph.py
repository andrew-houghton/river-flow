import pickle
from algorithms.lake import generate_lake


graph = pickle.load(open('graph.pkl', 'rb'))


def flood(point):
    points_in_lake = generate_lake(point)
    # TODO Merge the list of points in the lake into one point

# 1. Start by creating inflow list for each node
for i in graph.descending():
    i.inflow = []
for i in graph.descending():
    for j in i.outflow:
        j.inflow.append(i)


# 2. Find points with no outflow
for i in graph.descending():
    if len(i.outflow) == 0:
        flood(i)
