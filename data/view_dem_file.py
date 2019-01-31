import tifffile as tiff
from PIL import Image
import bz2
import os

path=os.path.dirname(os.path.abspath(__file__))+'/'

data=bz2.decompress(open(path+'dem.tif.bz2','rb').read())
with open(path+'dem2.tif','wb') as handle:
    handle.write(data)

im=tiff.imread(path+'dem2.tif')
im2 = im.astype('int32')
print(im2.max())
print(im2.min())
Image.fromarray(im2,'I').show()
