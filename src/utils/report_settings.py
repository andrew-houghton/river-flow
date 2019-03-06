def report_settings(size, frequency, job_name):
    num_images = int(size[0]*size[1]/frequency)
    print(f"Num images: {num_images}")
    total_size = (size[0]*size[1]*num_images)/1000000
    if total_size > 1000:
        print(f"Total data size: {total_size/1000.0:.2f} GB")
    else:
        print(f"Total data size: {total_size:.2f} MB")
