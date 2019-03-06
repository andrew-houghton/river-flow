import ffmpeg
import os


def make_video(job_name, file_format='avi', quality=3):
    images_folder = f"{os.path.dirname(os.path.dirname(os.path.abspath('')))}/data/{job_name}/"
    out_folder = f"{os.path.dirname(os.path.dirname(os.path.abspath('')))}/data/video/"
    video_filename = f'{out_folder}{job_name}.{file_format}'

    (
        ffmpeg
        .input(f'{images_folder}*.tiff', pattern_type='glob', framerate=25)
        .output(video_filename, **{'qscale:v': quality})
        .overwrite_output()
        .run()
    )
    print(f"Saved video to video_filename")
