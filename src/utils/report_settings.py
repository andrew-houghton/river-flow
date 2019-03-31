def report_settings(config):
    size = config['size']
    num_images = int(size[0]*size[1]/config['frequency'])
    print(f"Num images: {num_images}")
    total_size = (size[0]*size[1]*num_images)/1000000
    if total_size > 1000:
        print(f"Total data size: {total_size/1000.0:.2f} GB")
    else:
        print(f"Total data size: {total_size:.2f} MB")
