'''
Global constants for computer vision software. This file contains numerical constants used, error strings, and output
strings. Do NOT change any of these values.

Author: Hayden Banting
Version: 14 October 2017
'''
########################################################################################################################
import numpy as np
########################################################################################################################
GREEN = np.array([0, 255, 0])               # BGR colour format for green
BLUE = np.array([255, 0, 0])                # BGR colour format for blue
RED = np.array([0, 255, 255])               # BGR colour format for red
ACCEPT_GREEN_RANGE = np.array([72, 255])    # Acceptable hue ranges for green channel
ACCEPT_BLUE_RANGE = np.array([0, 175])      # Acceptable hue ranges for blue channel
ACCEPT_RED_RANGE = np.array([0, 178])       # Acceptable hue ranges for red channel
CALIBRATION_OFFSET = 0.56
########################################################################################################################
ERROR_LOAD_IMAGE = 'Error 0: Failed to load image. Ensure camera is connected correctly.'
WARNING_EXCEED_COMP_TIME_CLR = 'Colour algorithm exceeded allowed computation time.'
WARNING_EXCEED_COMP_TIME_FREQ = 'Freq algorithm exceeded allowed computation time.'
########################################################################################################################
STRING_TOTAL_PROCESSING_TIME = 'Total elapsed time: {}'
STRING_TOTAL_CLR_PROCESS_TIME = 'Total time to analyze using colour: {}\n'
STRING_TOTAL_FREQ_PROCESS_TIME = 'Total time to analyze using freq: {}\n'
STRING_IMAGE_LOAD_TIME = 'Time to load image: {}\n'
STRING_OBSTACLE_FIND_TIME = 'Time to process obstacles as nodes: {}'
STRING_KMEANS_LEARN_TIME = 'Time to finish kmeans unsupervised learning: {}'
STRING_SUBIMAGE_PROCESS_TIME = 'Time to process subimage ({},{}): {}'
STRING_LOWPASS_FILTER_TIME = 'Time to apply low-pass blur to image: {}'
STRING_GREYSCALE_TIME = 'Time to convert colour image to binary: {}'
STRING_FFT_TIME = 'Time to compute the 2D fft: {}'
STRING_FREQ_ANAL_TIME = 'Time to complete analysis in frequency domain: {}'
STRING_CLUSTER_GROUP_FORMAT = ' (k={})'
STRING_CAPTURED_IMAGE_FILE = 'img_{}_loc({})_ang(phi={}).jpg'
########################################################################################################################
DEG_TO_RAD = 0.0174532925
RAD_TO_DEG = 57.29577951
########################################################################################################################