import ffmpeg
import os
from PIL import Image as Img
from IPython.core.display import display
import numpy as np


out_folder = f"{os.path.dirname(os.path.dirname(os.path.abspath('')))}/data/video/"

def make_video(job_name, file_format='avi', quality=3):
    images_folder = f"{os.path.dirname(os.path.dirname(os.path.abspath('')))}/data/{job_name}/"
    video_filename = f'{out_folder}{job_name}.{file_format}'

    (
        ffmpeg
        .input(f'{images_folder}*.tiff', pattern_type='glob', framerate=25)
        .output(video_filename, **{'qscale:v': quality})
        .overwrite_output()
        .run()
    )
    print(f"Saved video to video_filename")

def make_image(job_name, heights):
    data = heights.astype(np.float64) / heights.max()
    data = 255 * data
    im = Img.fromarray(data.astype(np.uint8))
    im.save(f'{out_folder}{job_name}.png')