'''
Parameters which determine how output is handled. Options for displaying output for every intermediate step of the
algorithm. Plot titles and axis labels can also be changed here to fit an example more appropriately if required.

Author: Hayden Banting
Version: 28 October 2017
'''
########################################################################################################################
## Output Plot Toggles
########################################################################################################################
DISPLAY_ORIGINAL = 0                # Whether or not to display original image (both)
DISPLAY_SUB_IMGS = 0                # Whether or not to display sub-images (colour)
DISPLAY_CLUSTERS = 0                # Whether or not to display individual cluster images (colour)
DISPLAY_OBSTACLES = 0               # Whether or not to display obstacles images (colour)
DISPLAY_LOWPASS_BLUR = 0            # Whether or not to display obstacles images(freq)
DISPLAY_HIGHPASS_FILTERED = 0       # Whether or not to display obstacles images (freq)
DISPLAY_COLOUR_NODES = 0            # Whether or not to display output nodes (colour)
DISPLAY_FREQ_NODES = 0              # Whether or not to display output nodes (freq)
DISPLAY_NODAL_OBSTACLE = 0          # Whether or not to display the a collection of points representing the obstacle
########################################################################################################################
## Output Plot Options
########################################################################################################################
ORIGINAL_IMAGE_TITLE = 'Original Image'             # Title of original image plot
SUBIMAGE_TITLE = 'Sub-Image'                        # Title of subimage plot (by default includes sub-img index)
CLUSTER_TITLE = 'Image Parsed by Cluster Group'     # Title of cluster group (by default include cluster index)
LOWPASS_TITLE = 'Image After Low-Pass Blur'         # Title of blurred image
MAG_SPEC_TITLE = 'Magnitude Spectrum'               # Title for magnitude spectrum plots
PWR_SPEC_TITLE = 'Power Spectrum'                   # Title for power spectrum plots
HIGHPASS_TITLE = 'Image After Filtering'            # Title of image after high-pass filter (and additional filters)
OBSTACLE_TITLE = 'Obstacles Found in Image'         # Title of found obstacle plot
NODAL_OBSTACLE_TITLE = 'Points Outlining Obstacle'  # Title of nodal obstacle representation plot
NODAL_CLR_TITLE = 'Points Found by Colour'          # Title of nodal obstacle representation plot using colour only
NODAL_FREQ_TITLE = 'Points Found by Freq'           # Title of nodal obstacle representation plot using freq only
IMAGE_XLABEL = 'x [pixels]'                         # X-axis label of image plots
IMAGE_YLABEL = 'y [pixels]'                         # Y-axis label of image plots
POS_XLABEL = 'relative x [m]'                       # An axis describing relative x positions
POS_YLABEL = 'relative y [m]'                       # An axis describing relative y positions
SPECTRUM_LABEL = '|img| dB'                         # Label for an dB log axis
FREQ_LABEL = 'f [Hz]'                               # Label for a frequency axis
########################################################################################################################
## Output Print Toggles
########################################################################################################################
PRINT_TOTAL_PROCESSING_TIME = 0     # Whether or not to print total processing time (both)
PRINT_IMAGE_LOAD_TIME = 0           # Whether or not to print image loading time (both)
PRINT_OBSTACLE_FIND_TIME = 0        # Whether or not to print obstacle find time (both)
PRINT_DETECTED_OBSTACLE = 0         # Whether or not to print if an obstacle is detected in a sub-image (both)
PRINT_KMEANS_LEARN_TIME = 0         # Whether or not to print kmeans learning on sub-image time (colour)
PRINT_SUBIMAGE_PROCESS_TIME = 0     # Whether or not to print obstacle detection on sub-image (colour)
PRINT_LOWPASS_FILTER_TIME = 0       # Whether or not to print low pass filter blur time (freq)
PRINT_FFT_TIME = 0                  # Whether or not to print 2D fft time (freq)
PRINT_FREQ_ANAL_TIME = 0            # Whether or not to print 2D ifft time (freq)
PRINT_GREYSCALE_TIME = 0            # Whether ot no to print the time to convert to a gray scale image (freq)

