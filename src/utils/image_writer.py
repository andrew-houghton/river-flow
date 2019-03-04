import os
from PIL import Image as Img

class ImageWriter(object):
    def __init__(self, size, save_frequency, job_name, colour_function):
        path = f"{os.path.dirname(os.path.dirname(os.path.abspath('')))}/data/{job_name}/"
        if not os.path.exists(path):
            os.makedirs(path)
        print(f"Writer will save images to {path}")
        self.write_path = path
        self.index = 0
        self.image = Img.new('L', (size, size))
        self.pixels = self.image.load()
        self.save_frequency=save_frequency
        self.image_number = 0
        self.size = size
        self.previous_percent = 0
        self.colour_function = colour_function

    def update(self, node):
        self.index += 1
        self.pixels[node.home[0],node.home[1]] = self.colour_function(node.flow)
        if self.index % self.save_frequency == 0:
            filename = f"{self.write_path}{self.image_number}.tiff"
            (self.image).save(filename)
            percent_finished = int(self.index*100/self.size**2)
            if percent_finished != self.previous_percent and percent_finished%2==0:
                print(f'Processed {percent_finished}% of {self.size**2} images.')
                self.previous_percent = percent_finished
            self.image_number += 1