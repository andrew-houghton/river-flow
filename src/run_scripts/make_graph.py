#!/usr/bin/env python
# coding: utf-8

import pickle
from data_structures.location_graph import LocationGraph
from utils.load_image import load_and_crop_data
from utils.report_settings import report_settings


# Params
config = {
    'size': (1000, 1000),
    'offset': (0, 0),
    'frequency': 8000,
    'job_name': "run_scripts"
}

report_settings(config)
height_map = load_and_crop_data(config).tolist()

graph = LocationGraph(height_map, config)

def save(graph):
    import resource
    import sys
    print(resource.getrlimit(resource.RLIMIT_STACK))
    print(sys.getrecursionlimit())
    size = graph.config.size
    max_rec = 10*size[0]*size[1]
    resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
    sys.setrecursionlimit(max_rec)
    pickle.dump(graph, open('graph.pkl', 'wb'))