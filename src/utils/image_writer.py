import os
from PIL import Image as Img


class ImageWriter(object):
    def __init__(self, config, colour_function):
        self.size = config['size']
        self.save_frequency=config['frequency']

        path = f"{os.path.dirname(os.path.dirname(os.path.abspath('')))}/data/{config['job_name']}/"
        if not os.path.exists(path):
            os.makedirs(path)

        print(f"Writer will save images to {path}")
        self.write_path = path
        self.index = 0
        self.image = Img.new('RGB', self.size)
        self.pixels = self.image.load()
        self.image_number = 0
        self.previous_percent = 0
        self.colour_function = colour_function

    def __enter__(self):
        self._save()
        return self
    
    def __exit__(self, type, value, traceback):
        self._save()

    def update(self, node):
        self.index += 1
        node_colour = self.colour_function(node.flow)

        for i in node.position:
            self.pixels[i[0],i[1]] = node_colour
        
        if self.index % self.save_frequency == 0:
            self._save()

    def _save(self):
        filename = f"{self.write_path}{self.image_number:03}.tiff"
        (self.image).save(filename)
        self.image_number += 1

