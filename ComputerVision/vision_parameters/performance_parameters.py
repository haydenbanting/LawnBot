'''
Parameters which directly affect the computational accuracy of the obstacle detection algorithms.

Author: Hayden Banting
Version: 01 March 2018
'''
########################################################################################################################
## General Parameters
########################################################################################################################
RESOLUTION = (640, 480)             # Resolution of captured image
METER_PER_PIXEL = 0.00119           # Conversion ratio of metric meter to capture image pixel ratio
########################################################################################################################
## Default Number of Points to Produce
########################################################################################################################
N_COLOUR_POINTS = 30    # Number of  equally spaced points tracing outline of obstacle
N_FREQ_POINTS = 30      # Number of  equally spaced points tracing outline of obstacle
MAX_COMP_TIME_FREQ = 5  # Maximum time the freq algorithm can run in seconds
USE_CLR = 1             # Whether or not to use the colour algorithm
USE_FREQ = 1            # Whether or not to use the freq algorithm
########################################################################################################################
## Colour Algorithm Parameters
########################################################################################################################
N_CLUSTERS = 2          # Number of unsupervised cluster partitions (k argument)
TOL = 0.01              # Accuracy of colour detection
MAX_COMP_TIME_CLR = 5   # Maximum time the colour algorithm can run in seconds
########################################################################################################################
## Frequency Algorithm Parameters
########################################################################################################################
LOWPASS_FILTER_STRNEGTH = 9         # Increasing this parameter will increase the filtering strength (must be odd)
HIGHPASS_WINDOW_SIZE = [100, 100]   # Increasing will increase the high-pass strength (x, y)
CONTRAST_THRESHOLD = 0.25            # Values below a contrast percent w.r.t to maximum value are ignored (noise)
SMALL_OBSTACLE = 0.0005             # If a detected obstacle is smaller than % of the image size then ignore it
SEARCH_FOR_SMALL_ROWS = 5           # When searching for smalls, consider i rows of original image
SEARCH_FOR_SMALL_COLS = 5           # When searching for smalls, consider j cols of original image
BUFFER = 0.3                        # Percent of image around boundary to ignore (gets rid of fft singularities)
