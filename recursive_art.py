"""Computational Art Project

Generates a series of functions used to create images, stored in the images folder.
The images are then combined into a single video.

Dependencies:
Python 2.7
PIL library

To Run:
On Mac OSX, navigate to the directory and run 'python recursive_art.py'
"""

import random
import math
from PIL import Image
import os


def build_random_function(min_depth, max_depth, counter=0):
    """Build a random function.

    Builds a random function of depth at least min_depth and depth at most
    max_depth. (See the assignment write-up for the definition of depth
    in this context)

    Args:
        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function

    Returns:
        The randomly generated function represented as a nested list.
        (See the assignment writ-eup for details on the representation of
        these functions)
    """
    depth = random.randint(min_depth, max_depth)

    funcs = [lambda x, y, t: (t/10.0 + 1) * math.cos(math.pi * min((y+2)**2 / 10., 20) * x),  
            lambda x, y, t: (t/10.0 + 1) * math.sin(math.pi * min(x/5.0, 20) * y)]
            
    end_funcs = [lambda x, y, t: x, lambda x, y, t: y]

    if (counter < depth - 1):
        func = random.choice(funcs)
        counter += 1
        inp1 = build_random_function(min_depth, max_depth, counter)
        inp2 = build_random_function(min_depth, max_depth, counter)
        return lambda x, y, t: func(inp1(x, y, t), inp2(x, y, t), t)
    else:
        return lambda x, y, t: random.choice(end_funcs)(x, y, t)


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """Remap a value from one interval to another.
        
        Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].
        
        Args:
        val: the value to remap
        input_interval_start: the start of the interval that contains all
        possible values for val
        input_interval_end: the end of the interval that contains all possible
        values for val
        output_interval_start: the start of the interval that contains all
        possible output values
        output_inteval_end: the end of the interval that contains all possible
        output values
        
        Returns:
        The value remapped from the input to the output interval
        
        Examples:
        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    #check to make sure range isn't 0
    assert (input_interval_start != input_interval_end and output_interval_start != output_interval_end)
    
    #fix cases where input min > max and vice versa
    #numbers multiplied by 1.0 to ensure float conversion
    inp_int_start = min(input_interval_start, input_interval_end) * 1.0
    inp_int_end = max(input_interval_start, input_interval_end) * 1.0
    out_int_start = min(output_interval_start, output_interval_end) * 1.0
    out_int_end = max(output_interval_start, output_interval_end) * 1.0
    
    remapped = (val - inp_int_start) * (out_int_end-out_int_start)/(inp_int_end - inp_int_start) + out_int_start
    return remapped


def color_map(val):
    """Maps input value between -1 and 1 to an integer 0-255, suitable for use as an RGB color code.

    Args:
        val: value to remap, must be a float in the interval [-1, 1]

    Returns:
        An integer in the interval [0,255]

    Examples:
        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def generate_art(filename, x_size=350, y_size=350):
    """Generate computational art and save as an image file.

    Args:
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    #red_function = ["x"]
    #green_function = ["y"]
    #blue_function = ["x"]

    red_green_blue = [build_random_function(3, 5),
                build_random_function(3, 5), 
                build_random_function(3, 5)]

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    time = 24 # how many frames to be generated
    assert time > 1 # to ensure at least 1 image is generated
    for t in range(1, time+1):
        for i in range(x_size):
            for j in range(y_size):
                x = remap_interval(i, 0, x_size, -1, 1)
                y = remap_interval(j, 0, y_size, -1, 1)
                pixels[i, j] = (tuple(color_map(color_func(x, y, t)) for color_func in red_green_blue))
        while len(str(t)) < 3:
            t = "0" + str(t)
        
        fullpath = os.path.join(os.path.dirname(__file__), 'images/')
        im.save(fullpath + "frame{time}.png".format(time=t))


    os.system("ffmpeg -r 3 -i {path}frame%03d.png -vcodec mpeg4 -y {name}.mp4".format(path=fullpath, name=filename))

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart")

