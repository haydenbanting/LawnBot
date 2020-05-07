'''
Some postr-processing filters for improving obstacle detection. Note: Functions still need documentation.

Author: Hayden Banting
Version: 02 November 2017
'''
########################################################################################################################
import numpy as np
from ComputerVision.vision_parameters import performance_parameters as pp
########################################################################################################################
def remove_small_objects(image, height, width):
    for irow in range(0, pp.SEARCH_FOR_SMALL_ROWS):
        for jcol in range(0, pp.SEARCH_FOR_SMALL_COLS):
            size = np.count_nonzero(image[irow * np.int(height / pp.SEARCH_FOR_SMALL_ROWS):
                                    (1 + irow) * np.int(height / pp.SEARCH_FOR_SMALL_ROWS),
                                    jcol * np.int(width / pp.SEARCH_FOR_SMALL_COLS):
                                    (1 + jcol) * np.int(width / pp.SEARCH_FOR_SMALL_COLS)])
            if size < height * width * pp.SMALL_OBSTACLE:
                image[irow * np.int(height / pp.SEARCH_FOR_SMALL_ROWS):
                (1 + irow) * np.int(height / pp.SEARCH_FOR_SMALL_ROWS),
                jcol * np.int(width / pp.SEARCH_FOR_SMALL_COLS):
                (1 + jcol) * np.int(width / pp.SEARCH_FOR_SMALL_COLS)] = 0
    return image
########################################################################################################################
def remove_numerical_noise(image):
    image[image < pp.CONTRAST_THRESHOLD * image.max()] = 0
    return image
########################################################################################################################
def remove_fft_singularities(image, height, width):
    image[:, 0:np.int(pp.BUFFER * width / 4)] = 0
    image[:, width - np.int(pp.BUFFER * width / 4):width] = 0
    image[0:np.int(pp.BUFFER * height / 4), :] = 0
    image[height - np.int(pp.BUFFER * height / 4):height, :] = 0
    return image
########################################################################################################################