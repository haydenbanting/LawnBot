'''
Main script for object detection via colour analysis.

Author: Hayden Banting
Version: 07 January 2018
'''
########################################################################################################################
## Imports
########################################################################################################################
import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from ComputerVision.constants import constants as const
from ComputerVision.image_utilities import image_functions
from ComputerVision.vision_parameters import output_parameters as op
from ComputerVision.vision_parameters import performance_parameters as pp
from ComputerVision.postprocessing import image_to_points
from ComputerVision.postprocessing import data_set
from ComputerVision.postprocessing import post_filtering
from ComputerVision.timing import timeout
########################################################################################################################
@timeout.timeout(pp.MAX_COMP_TIME_CLR, const.WARNING_EXCEED_COMP_TIME_CLR)
def main(img, num_points, cur_location, cur_angle):
    '''
    This function takes an input image, parses it by its colour properties, performs the obstacle detection algorithm,
    and then finally returns a number of points describing the obstacles (if found) location relative to some origin.
    There are several intermediate plots and outputs which can toggled via the vision_paramaters files.

    :param img: input image to analyze [np.array N x M x p)
    :param num_points: number of points to represent obstacles [scalar]
    :param cur_location: relative current location [scalar]
    :param cur_angle:  relative current angle [scalar]
    :return: data_points: array of objects describing obstacle [np.array 1 x N]
    '''
    if not pp.USE_CLR: return np.array([])
    start_time = time.time()
    ####################################################################################################################
    ## Set-up
    ####################################################################################################################
    # Computes the subplot code for the first sub plot (XYZ: X - Subplot rows,  Y - subplot cols, Z - subplot index)
    max_sub_plots_code = 100 * pp.N_CLUSTERS + 10 + 1

    # Initialize structure
    data_points = np.array([])

    # Get some image information
    height, width, dim = image_functions.get_image_dimensions(img)
    ####################################################################################################################
    ## K-means clustering vector quantization of image
    ####################################################################################################################
    process_time = time.time()

    # Reshape from 3D matrix into 2D matrix where all colour information for a single dimension is in 1D vector
    img_vec = np.reshape(img, [height * width, dim])

    # Unsupervised cluster to sort image into k groups
    kmeans = KMeans(n_clusters=pp.N_CLUSTERS)
    kmeans.fit(img_vec)

    if op.PRINT_KMEANS_LEARN_TIME:
        print(const.STRING_KMEANS_LEARN_TIME.format(time.time() - process_time))

    ####################################################################################################################
    ## Checking each cluster for obstacles
    ####################################################################################################################
    process_time = time.time()

    for k in range(pp.N_CLUSTERS):

        # Create a vector of containing only data which belongs to cluster k
        cur_cluster = 0 * img_vec
        cur_cluster[np.where(kmeans.labels_ == k), :] = img_vec[np.where(kmeans.labels_ == k), :]

        # Reshape vector back into image matrix
        cur_cluster = np.reshape(cur_cluster, [height, width, dim])

        if op.DISPLAY_CLUSTERS:
            fig = plt.figure(2000)
            ax = fig.add_subplot(max_sub_plots_code + k)
            ax.imshow(cur_cluster[..., ::-1])
            fig.suptitle((op.CLUSTER_TITLE + const.STRING_CLUSTER_GROUP_FORMAT).format(pp.N_CLUSTERS))

        # Check if cluster should be filtered (in allowed hue range)
        cur_mean_blue_hue, cur_mean_green_hue, cur_mean_red_hue = kmeans.cluster_centers_[k]  # [B, G, R]
        blue_allowed, green_allowed, red_allowed = [0, 0, 0]
        if const.ACCEPT_BLUE_RANGE[0] * (1 - pp.TOL) < cur_mean_blue_hue < const.ACCEPT_BLUE_RANGE[1] * (
            1 + pp.TOL):
            blue_allowed = 1
        if const.ACCEPT_GREEN_RANGE[0] * (1 - pp.TOL) < cur_mean_green_hue < const.ACCEPT_GREEN_RANGE[1] * (
            1 + pp.TOL):
            green_allowed = 1
        if const.ACCEPT_RED_RANGE[0] * (1 - pp.TOL) < cur_mean_red_hue < const.ACCEPT_RED_RANGE[1] * (
            1 + pp.TOL):
            red_allowed = 1


        if blue_allowed and green_allowed and red_allowed:
            pass
        else:
            # Remove very small obstacles (don't consider very small obtsacles which consist of a few pixels)
            cur_cluster = post_filtering.remove_small_objects(cur_cluster, height, width)

            # Represent an obstacle by n points points around
            data_points = np.append(data_points, image_to_points.obstacle_cluster_to_points(cur_cluster, height, width,
                                                                                   cur_location, cur_angle, num_points))

            if op.DISPLAY_OBSTACLES:
                fig = plt.figure(3000)
                ax = fig.add_subplot(max_sub_plots_code + k)
                ax.imshow(cur_cluster[..., ::-1])
                fig.suptitle(op.OBSTACLE_TITLE)

    if op.DISPLAY_COLOUR_NODES:
        data_set.plot_data_set(data_points, height, width, cur_location, cur_angle, 3, op.NODAL_CLR_TITLE)

    if op.PRINT_OBSTACLE_FIND_TIME:
        print(const.STRING_OBSTACLE_FIND_TIME.format(time.time() - process_time))

    if op.PRINT_TOTAL_PROCESSING_TIME:
        print(const.STRING_TOTAL_CLR_PROCESS_TIME.format(time.time() - start_time))

    return data_points
########################################################################################################################