'''
This function contains numerous utility functions for updating/changing the computer vision parameters. Motivated by
practical calibration practices, these functions will be needed required by the python-side of the GUI wireless
interface. By using these functions python-side of the GUI can modify key computer vision performance parameters
allowing us to update parameters (effectively calibrate) during field tests.

Author: Hayden Banting
Version: 06 January 2018
'''
from ComputerVision.vision_parameters import input_parameters, output_parameters, performance_parameters
########################################################################################################################
def update_camera_resolution(resolution=performance_parameters.RESOLUTION):
    '''
    This function updates the camera resolution.

    :param resolution: A tuple representing the resolution (int, int)
    '''
    performance_parameters.RESOLUTION = resolution

def update_colour_algorithm_complexitiy(k=performance_parameters.N_CLUSTERS):
    '''
    This function updates the colour algorithm complexity by adjusting the number of clusters to sort by. More clusters
    will detect multiple objects easier at the cost of increased computational time.

    :param k: number of clusters (int)
    '''
    performance_parameters.N_CLUSTERS = k

def update_colour_algorithm_accuracy(tol=performance_parameters.TOL):
    '''
    Accuracy or tolerance of how lenient the algorithm is when determining if some area is an obstacle or not.
    Increasing the tolerance will make make the algorithm classify more area as obstacles, and less tolerance will be
    stricter on the obstacle criteria.

    :param tol: value between 0 and 1
    '''
    performance_parameters.TOL = tol

def update_freq_algorithm_contrast_threshold(thresh=performance_parameters.CONTRAST_THRESHOLD):
    '''
    Updates the minimum contrast the algorithm should look for when detecting obstacles. Large contrast indicates
    obstacles and small contrast likely not. Note that contrast is given as a percentage of whatever the maximum
    contrast detected is, and not an abosulte value.

    :param thresh: value between 0 and 1
    '''
    performance_parameters.CONTRAST_THRESHOLD = thresh

def update_freq_algorithm_small_obstacle(small=performance_parameters.SMALL_OBSTACLE):
    '''
    Updates the size of what is considered "small obstacles" to be ignored. Very small areas with significant contrast
    are ignored. These usually occur surrounding an actual obstacles and ignoring them will smooth the obstacle
    boundary.

    :param small: percentage of image, value from 0 to 1
    '''
    performance_parameters.SMALL_OBSTACLE = small

def update_freq_algorithm_buffer(buffer = performance_parameters.BUFFER):
    '''
    Updates the parameter which removes the fft singularity at the image boundary. If selected to small a false
    obstacle will be detected at the image boundary.

    :param buffer: percentage of image, value from 0 to 1
    '''
    performance_parameters.BUFFER = buffer


