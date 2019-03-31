from PIL import TiffImagePlugin
from PIL import Image as Img
import bz2
import os
import numpy as np


def load_image_data() -> TiffImagePlugin.TiffImageFile:
    path = os.path.dirname(os.path.abspath('')) + '/data/'
    data = bz2.decompress(open(path + 'dem.tif.bz2', 'rb').read())
    with open(path + 'dem2.tiff', 'wb') as handle:
        handle.write(data)
    return Img.open(path + 'dem2.tiff')

def load_and_crop_data(config: dict):
    size, offset = config['size'], config['offset']
    raw_height_array = np.asarray(load_image_data())
    return raw_height_array[offset[0]:offset[0]+size[0], offset[1]:offset[1]+size[1]]
