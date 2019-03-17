import bz2
import os
import numpy as np
import tifffile as tiff
from PIL import Image

def rescale(im4):
    data = im4.astype(np.float64)
    data = data - data.min()
    data = data / data.max()
    data = 255 * data
    data = data.astype(np.uint8)
    # data = np.fliplr(data)
    # data = np.rot90(data)
    return data


path = os.path.dirname(os.path.abspath(__file__)) + '/'

data = bz2.decompress(open(path + 'dem.tif.bz2', 'rb').read())
with open(path + 'dem2.tif', 'wb') as handle:
    handle.write(data)

im = tiff.imread(path + 'dem2.tif')
im2 = im.astype('int32')
print(im2.shape)

i, j = 890, 890
im3 = rescale(im2[0:i, 0:i])
image = Image.fromarray(im3)
image.show()
