'''
Main script for computer vision package.

Author: Hayden Banting
Version: 05 November 2017
'''
########################################################################################################################
## Imports
import os
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
from ComputerVision import main_colour
from ComputerVision import main_frequency
from ComputerVision import main_camera
from ComputerVision.constants import constants as const
from ComputerVision.image_utilities import image_functions
from ComputerVision.postprocessing import data_set
from ComputerVision.vision_parameters import output_parameters as op
from ComputerVision.vision_parameters import input_parameters as ip
from ComputerVision.vision_parameters import performance_parameters as pp
########################################################################################################################
def main_computer_vision(n_colour_points=pp.N_COLOUR_POINTS, n_freq_points=pp.N_FREQ_POINTS,
                         cur_location=ip.DEFAULT_START_LOCATION, cur_angle=ip.DEFAULT_START_ANGLE):

    img_num = 1 # Hard coded for now

    start_time = time.time()

    ## Capture Image Using RPi Camera
    main_camera.capture_image(img_num, cur_location, cur_angle)

    ## Load captured image as a multi-dim array
    img = image_functions.load_image(os.path.join(ip.FILEPATH,
                                     const.STRING_CAPTURED_IMAGE_FILE.format(img_num, cur_location, cur_angle)), 1)
    
    img = cv2.flip(img, 0)
    img = cv2.flip(img, 1)
    
    
    assert (type(img) != type(None)), const.ERROR_LOAD_IMAGE
    height, width, dim = image_functions.get_image_dimensions(img)


    if op.PRINT_IMAGE_LOAD_TIME:
        print(const.STRING_IMAGE_LOAD_TIME.format(time.time() - start_time))

    if op.DISPLAY_ORIGINAL:
        plt.figure(1)
        plt.imshow(img[..., ::-1])
        plt.title(op.ORIGINAL_IMAGE_TITLE)
        plt.xlabel(op.IMAGE_XLABEL)
        plt.ylabel(op.IMAGE_YLABEL)


    # Perform colour analysis
    colour_data = main_colour.main(img, n_colour_points, cur_location, cur_angle)

    # Perform frequency analysis
    freq_data = main_frequency.main(img, n_freq_points, cur_location, cur_angle)

    # Combine data from each
    obstacle_data = np.concatenate((colour_data, freq_data))

    if op.DISPLAY_NODAL_OBSTACLE:
        data_set.plot_data_set(obstacle_data, height, width, cur_location, cur_angle)

    if op.PRINT_TOTAL_PROCESSING_TIME:
        print(const.STRING_TOTAL_PROCESSING_TIME.format(time.time()-start_time))

    plt.show()

    return obstacle_data
########################################################################################################################




