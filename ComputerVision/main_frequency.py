'''
Main function for object detection via frequency analysis.

Author: Hayden Banting
Version: 02 December 2017
'''
########################################################################################################################
## Imports
########################################################################################################################
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
from ComputerVision.constants import constants as const
from ComputerVision.image_utilities import image_functions
from ComputerVision.vision_parameters import output_parameters as op
from ComputerVision.vision_parameters import performance_parameters as pp
from ComputerVision.postprocessing import data_set
from ComputerVision.postprocessing import image_to_points
from ComputerVision.postprocessing import post_filtering
from ComputerVision.timing import timeout
########################################################################################################################
@timeout.timeout(pp.MAX_COMP_TIME_FREQ, const.WARNING_EXCEED_COMP_TIME_FREQ)
def main(img, num_points, cur_location, cur_angle):
    '''
    This function takes an input image, parses it by its frequency properties, performs the obstacle detection
    algorithm, and then finally returns a number of points describing the obstacles (if found) location relative to some
    origin. There are several intermediate plots and outputs which can toggled via the vision_paramaters files.

    :param img: input image to analyze [np.array N x M x p)
    :param num_points: number of points to represent obstacles [scalar]
    :param cur_location: relative current location [scalar]
    :param cur_angle:  relative current angle [scalar]
    :return: data_points : array of objects describing obstacle [np.array 1 x N]
    '''
    if not pp.USE_FREQ: return np.array([])
    start_time = time.time()
    ####################################################################################################################
    ## Set-up
    ####################################################################################################################
    # Get some image information
    height, width, dim = image_functions.get_image_dimensions(img)

    ####################################################################################################################
    ## Blurring (Low-pass)
    ####################################################################################################################
    process_time = time.time()
    # blur = cv2.blur(img, (3,3))
    # blur = cv2.bilateralFilter(img, 9, 300, 300)
    blur = cv2.medianBlur(img, pp.LOWPASS_FILTER_STRNEGTH)  # second arguemnt must be odd, increases filtering

    if op.DISPLAY_LOWPASS_BLUR:
        plt.figure(5000)
        plt.imshow(blur[..., ::-1])
        plt.title(op.LOWPASS_TITLE)
        plt.xlabel(op.IMAGE_XLABEL)
        plt.ylabel(op.IMAGE_YLABEL)
        plt.colorbar(plt.imshow(blur[..., ::-1]))

    if op.PRINT_LOWPASS_FILTER_TIME:
        print(const.STRING_LOWPASS_FILTER_TIME.format(time.time() - process_time))
    ####################################################################################################################
    ## Grey-Scale Conversion
    ####################################################################################################################
    process_time = time.time()
    grey = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    if op.PRINT_GREYSCALE_TIME:
        print(const.STRING_GREYSCALE_TIME.format(time.time()- process_time))
    ####################################################################################################################
    ## Fourier Transform (2D)
    ####################################################################################################################
    process_time = time.time()
    f = np.fft.fft2(grey)

    if op.PRINT_FFT_TIME:
        print(const.STRING_FFT_TIME.format(time.time() - process_time))
    ####################################################################################################################
    ## Frequency Domain Analysis (Edge detection, filters, inverse transform)
    ####################################################################################################################
    process_time = time.time()
    # Shift the spectrum so the zero frequency component is centered
    fshift = np.fft.fftshift(f)

    # Apply a high pass filter to the spectrum
    cheight, cwidth = height / 2, width / 2
    fshift[np.int(cheight - pp.HIGHPASS_WINDOW_SIZE[0] / 2):np.int(cheight + pp.HIGHPASS_WINDOW_SIZE[0] / 2),
    np.int(cwidth - pp.HIGHPASS_WINDOW_SIZE[1] / 2):np.int(cwidth + pp.HIGHPASS_WINDOW_SIZE[1] / 2)] = 0

    # Inverse shift of the spectrum
    f_ishift = np.fft.ifftshift(fshift)

    # Inverse transfrom to obtain filtered image
    img_filtered = np.fft.ifft2(f_ishift)
    img_filtered = np.abs(img_filtered)

    # Pad the boundaries of the image with zeros (removes the singularities of the fft at image boundary)
    img_filtered = post_filtering.remove_fft_singularities(img_filtered, height, width)

    # Remove non-significant contrast (essentially removing noise and near-zero values in image array)
    img_filtered = post_filtering.remove_numerical_noise(img_filtered)

    # Remove very small obstacles (do not consider very small obtsacles which consist on only a few pixels)
    img_filtered = post_filtering.remove_small_objects(img_filtered, height, width)

    if op.DISPLAY_HIGHPASS_FILTERED:
        plt.figure(6000)
        plt.imshow(img_filtered)
        plt.title(op.HIGHPASS_TITLE)
        plt.xlabel(op.IMAGE_XLABEL)
        plt.ylabel(op.IMAGE_YLABEL)
        plt.colorbar(plt.imshow(img_filtered))

    if op.PRINT_FREQ_ANAL_TIME:
        print(const.STRING_FREQ_ANAL_TIME.format(time.time() - process_time))
    ####################################################################################################################
    ## Representing Obstacles as Nodal Data
    ####################################################################################################################
    process_time = time.time()

    try:
        data_points = image_to_points.obstacle_outline_to_points(img_filtered, height, width, cur_location, cur_angle,
                                                                 num_points)
    except:
        data_points = np.array([])

    if op.PRINT_OBSTACLE_FIND_TIME:
        print(const.STRING_OBSTACLE_FIND_TIME.format(time.time() - process_time))
    ####################################################################################################################
    ## Finishing up (optional outputs)
    ####################################################################################################################
    if op.DISPLAY_FREQ_NODES:
        data_set.plot_data_set(data_points, height, width, cur_location, cur_angle, 4, op.NODAL_FREQ_TITLE)

    if op.PRINT_TOTAL_PROCESSING_TIME:
        print(const.STRING_TOTAL_FREQ_PROCESS_TIME.format(time.time() - start_time))

    return data_points
########################################################################################################################