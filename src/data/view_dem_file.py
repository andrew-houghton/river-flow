import os

import bz2
import tifffile as tiff
from PIL import Image

path = os.path.dirname(os.path.abspath(__file__)) + '/'

data = bz2.decompress(open(path + 'dem.tif.bz2', 'rb').read())
with open(path + 'dem2.tif', 'wb') as handle:
    handle.write(data)

im = tiff.imread(path + 'dem2.tif')
im2 = im.astype('int32')
print(im2.shape)

i, j = 3400, 800
im3 = im2[i - j:i, i - j:i]
image = Image.fromarray(im3, 'I')
image.show()
