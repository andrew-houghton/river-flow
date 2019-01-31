import tifffile as tiff
from PIL import Image
import bz2

# unzip
data=bz2.decompress(open('dem.tif.bz2','rb').read())
with open('dem2.tif','wb') as handle:
    handle.write(data)

im=tiff.imread('dem2.tif')
im2 = im.astype('int32')
Image.fromarray(im2,'I').show()
