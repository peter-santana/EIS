import numpy as np
import sys


def preproc(arr):
    """
    Ensure that the shape is correct for downstream pipeline.
    """
    
    s = arr.shape

    try:
        assert s[1] == 2048
        assert s[2] == 4102
    except AssertionError:
        print('Invalid shape. Received shape:', s) 
        print('Required shape: (x, 2048, 4102) where ', 
              'x is the number of images in stack.')
        print('This file may have to be skipped ', 
              'or processed separately. Exiting.')
        sys.exit(0)

    num_stack = int(s[0])

    # i.e., if data is actually just a single 2d image
    if num_stack == 1:
        arr = arr.reshape((s[1], s[2]))

        # Now pull out framegrabber columns
        arr = arr[:, 6:]

    # i.e., if data is actually a stack of 2d images
    elif num_stack > 1:
        print('Found', num_stack, 
              'images in stack. Returning median of stack.')
        arr = np.median(arr, axis=0)

        # Now pull out framegrabber columns
        arr = arr[:, 6:]

    s = arr.shape

    assert s[0] == 2048
    assert s[1] == 4096

    return arr
