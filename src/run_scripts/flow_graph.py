from tqdm import tqdm
from utils.colour import get_colour_function
from algorithms.flow import flow
from utils.dummy_writer import DummyWriter
from utils.image_writer import ImageWriter
from utils.load_image import load_and_crop_data
from utils.publish import make_video, make_image
import pickle


config = {
    'size': (1000, 1000),
    'offset': (0, 0),
    frequency: 8000,
    job_name: "run_scripts"
}

graph=pickle.load(open('graph.pkl', 'rb'))

nodes_with_flow = flow(graph, DummyWriter(), size)

flows = [n.flow for n in nodes_with_flow.ascending()]

with ImageWriter(size, frequency, job_name, get_colour_function(flows)) as imgWriter:
    for node in tqdm(graph.descending(), total=len(graph), unit=" nodes"):
        imgWriter.update(node)

make_video(job_name, quality=1)
make_image(job_name, load_and_crop_data(size, offset))
