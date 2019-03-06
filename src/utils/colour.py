from functools import partial
import math


def normalize_values(i, max_log_value):
    num_colours = 3
    i=math.log(i)*256/max_log_value
    val = int(i % 256)
    colour_ranges = [
        (val,0,0),
        (255,val,0),
        (255,255,val),
    ]
    category = int((i % 256*num_colours)/256)
    return colour_ranges[category]

def get_colour_function(flows):
    max_log_value = max([math.log(i) for i in flows])
    print(f"Max flow: {max(flows)}")
    print(f"Max log(flow): {max_log_value}")
    return partial(normalize_values, max_log_value=max_log_value)
