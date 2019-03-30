#!/usr/bin/env python
# coding: utf-8

# Imports
from tqdm import tqdm
from data_structures.location_graph import LocationGraph
from utils.dummy_writer import DummyWriter
from utils.image_writer import ImageWriter
from utils.const_writer import ConstWriter
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

def colour_func(num_points):
    return (0,0, min(num_points*20-20,255))

constWriter = ConstWriter(size, job_name, colour_func)

for node in tqdm(graph.descending(), total=len(graph), unit=" nodes"):
    constWriter.update(node)

constWriter.save()
im=load_and_crop_data(size, offset)
im = im - im.min()
make_image(job_name, im)
