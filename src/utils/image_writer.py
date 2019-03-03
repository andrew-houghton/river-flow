import numpy as np
from PIL import Image as Img


class ImageWriter(object):
    def __init__(self, path, size, save_frequency=10000):
        self.write_path = path
        self.index = 0
        self.arr = np.zeros((size,size))
        self.save_frequency=save_frequency

    def update(self, node):
        self.index += 1
        self.arr[node.home[0],node.home[1]] = 100
        if self.index % self.save_frequency == 0:
            im = Img.fromarray(self.arr, 'L')
            filename = f"{self.write_path}img{self.index}.tiff"
            im.save(filename)
            
            print(f"writer viewed {self.index} nodes")
            print(f"saved image {filename}")
