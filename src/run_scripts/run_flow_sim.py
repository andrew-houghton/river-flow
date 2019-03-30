#!/usr/bin/env python
# coding: utf-8

# Imports
from tqdm import tqdm

import sys
sys.path.append("../")

from algorithms.flow import flow
from data_structures.location_graph import LocationGraph
from utils.dummy_writer import DummyWriter
from utils.image_writer import ImageWriter
from utils.report_settings import report_settings
from utils.load_image import load_and_crop_data
from utils.colour import get_colour_function
from utils.publish import make_video, make_image

# Params
size = (890, 890)
offset = (0, 0)
frequency = 8000
job_name = "run_scripts"
report_settings(size, frequency, job_name)
height_map = load_and_crop_data(size, offset).tolist()

graph = LocationGraph(height_map)

nodes_with_flow = flow(graph, DummyWriter(), size)

flows = [n.flow for n in nodes_with_flow.ascending()]

with ImageWriter(size, frequency, job_name, get_colour_function(flows)) as imgWriter:
    for node in tqdm(graph.descending(), total=len(graph), unit=" nodes"):
        imgWriter.update(node)

make_video(job_name, quality=1)
make_image(job_name, load_and_crop_data(size, offset))
