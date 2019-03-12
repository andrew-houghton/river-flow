import os
from PIL import Image as Img


class ConstWriter(object):
    def __init__(self, size, job_name, colour_function):
        path = f"{os.path.dirname(os.path.dirname(os.path.abspath('')))}/data/{job_name}/"
        if not os.path.exists(path):
            os.makedirs(path)
        print(f"Writer will save images to {path}")
        self.write_path = path
        self.image = Img.new('RGB', size)
        self.pixels = self.image.load()
        self.colour_function = colour_function
        self.job_name = job_name

    def update(self, node):
        node_colour = self.colour_function(len(node.position))
        for i in node.position:
            self.pixels[i[0],i[1]] = node_colour

    def save(self):
        filepath = f"{self.write_path}{self.job_name}.tiff"
        (self.image).save(filepath)
        print(f"Saved const writer image to {image_filepath}")
