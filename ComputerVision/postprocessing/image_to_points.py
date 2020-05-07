'''
Post-processing utility functions for representing output obstacle data in different formats other than images.

Author: Hayden Banting
Version: 30 October 2017
'''
########################################################################################################################
import numpy as np
from ComputerVision.postprocessing import data_set
from ComputerVision.transforms import coordinate_transform as ct
########################################################################################################################
def obstacle_cluster_to_points(cluster, img_height, img_width, cur_location, cur_angle, n_points):
    '''
    This function takes in a cluster image was has already been determined to be an obstacle. It then represents the
    obstacle(s) present in that image as a collection of points where said points lay on the boundary of the
    obstacle(s).

    :param cluster: a cluster image [N x M x p int np.array]
    :param img_height: height of cluster image [int]
    :param img_width: width of cluster image [int]
    :param n_points: number of points to represent the image [int]
    :return: An array of data_point objects [1 x N class mp.array]
    '''

    # find the top of the obstacle by checking for first non-zero row from the top on the image
    for i in range(img_height):
        if np.sum(cluster[i,:,:]) != 0:
            top = i
            break

    # find the bottom of the obstacle by checking for first non-zero row from the bottom on the image
    for i in reversed(range(img_height)):
        if np.sum(cluster[i,:,:]) != 0:
            bottom = i
            break

    # find the left of the obstacle by checking for first non-zero column from the left on the image
    for j in range(img_width):
        if np.sum(cluster[:,j,:]) != 0:
            left = j
            break

    # find the right of the obstacle by checking for first non-zero column from the right on the image
    for j in reversed(range(img_width)):
        if np.sum(cluster[:,j,:]) != 0:
            right = j
            break

    # define equally spaced points from left to right and top to bottom
    x_defined = np.linspace(left, right, 0.25*n_points).astype(int)
    y_defined = np.linspace(top, bottom, 0.25 * n_points).astype(int)

    # build the zero-vectors which will be filled in once points have been found
    y_found_up = 0 * x_defined
    y_found_down = 0 * x_defined
    x_found_left = 0 * y_defined
    x_found_right = 0 * y_defined

    # find the set of y points for each fixed x-point in the defined x points
    for idx in range(np.alen(x_defined)):

        xpoint = x_defined[idx]

        for i in range(img_height):
            if np.sum(cluster[i, xpoint, :]) != 0:
                ypoint = i
                y_found_up[idx] = ypoint
                break

        for i in reversed(range(img_height)):
            if np.sum(cluster[i, xpoint, :]) != 0:
                ypoint = i
                y_found_down[idx] = ypoint
                break

    # find the set of x points for each fixed y-point in the defined y points
    for idx in range(np.alen(y_defined)):

        ypoint = y_defined[idx]

        for j in range(img_width):
            if np.sum(cluster[ypoint, j, :]) != 0:
                xpoint = j
                x_found_left[idx] = xpoint
                break

        for j in reversed(range(img_width)):
            if np.sum(cluster[ypoint, j, :]) != 0:
                xpoint = j
                x_found_right[idx] = xpoint
                break

    # initialize an empty array which will be filled with data_point objects
    data_points = np.array([])

    # create the data_point objects for each x-defined point set and add them to the array
    for idx in range(np.alen(x_defined)):
        data_points = np.append(data_points, data_set.data_point(ct.tranform_coordinate([x_defined[idx], y_found_up[idx]], img_height, img_width, cur_location, cur_angle), 1))
        data_points = np.append(data_points, data_set.data_point(ct.tranform_coordinate([x_defined[idx], y_found_down[idx]], img_height, img_width, cur_location, cur_angle), 1))

    # create the data_point objects for each y-defined point set and add them to the array
    for idx in range(np.alen(y_defined)):
        data_points = np.append(data_points, data_set.data_point(ct.tranform_coordinate([x_found_left[idx], y_defined[idx]], img_height, img_width, cur_location, cur_angle), 1))
        data_points = np.append(data_points, data_set.data_point(ct.tranform_coordinate([x_found_right[idx], y_defined[idx]], img_height, img_width, cur_location, cur_angle), 1))

    return data_points
########################################################################################################################
def obstacle_outline_to_points(image, img_height, img_width, cur_location, cur_angle, n_points):
    '''
    This function takes in an image were an obstacle has been detected and its boundary is defined.

    :param image: a grey scale image [N x M int np.array]
    :param img_height: height of cluster image [int]
    :param img_width: width of cluster image [int]
    :param n_points: number of points to represent the image [int]
    :return: An array of data_point objects [1 x N class mp.array]
    '''

    # Some default for if nothing is found
    left = 0
    right = 0
    top = 0
    bottom = 0

    # find the top of the obstacle by checking for first non-zero row from the top on the image
    for i in range(img_height):
        if np.sum(image[i,:]) != 0:
            top = i
            break

    # find the bottom of the obstacle by checking for first non-zero row from the bottom on the image
    for i in reversed(range(img_height)):
        if np.sum(image[i,:]) != 0:
            bottom = i
            break

    # find the left of the obstacle by checking for first non-zero column from the left on the image
    for j in range(img_width):
        if np.sum(image[:,j]) != 0:
            left = j
            break

    # find the right of the obstacle by checking for first non-zero column from the right on the image
    for j in reversed(range(img_width)):
        if np.sum(image[:,j]) != 0:
            right = j
            break

    # define equally spaced points from left to right and top to bottom
    x_defined = np.linspace(left, right, 0.25*n_points).astype(int)
    y_defined = np.linspace(top, bottom, 0.25 * n_points).astype(int)

    # build the zero-vectors which will be filled in once points have been found
    y_found_up = 0 * x_defined
    y_found_down = 0 * x_defined
    x_found_left = 0 * y_defined
    x_found_right = 0 * y_defined

    # find the set of y points for each fixed x-point in the defined x points
    for idx in range(np.alen(x_defined)):

        xpoint = x_defined[idx]
        found = 0
        while not found:
            for i in range(img_height):
                if np.sum(image[i, xpoint]) != 0:
                    ypoint = i
                    y_found_up[idx] = ypoint
                    found = 1
                    break
            xpoint = xpoint + 1 # adjust xpoint slightly if nothing found

        xpoint = x_defined[idx]
        found = 0
        while not found:
            for i in reversed(range(img_height)):
                if np.sum(image[i, xpoint]) != 0:
                    ypoint = i
                    y_found_down[idx] = ypoint
                    found = 1
                    break
            xpoint = xpoint + 1 # adjust xpoint slightly if nothing found

    # find the set of x points for each fixed y-point in the defined y points
    for idx in range(np.alen(y_defined)):

        ypoint = y_defined[idx]
        found = 0
        while not found:
            for j in range(img_width):
                if np.sum(image[ypoint, j]) != 0:
                    xpoint = j
                    x_found_left[idx] = xpoint
                    found = 1
                    break
            ypoint = ypoint + 1

        ypoint = y_defined[idx]
        found = 0
        while not found:
            for j in reversed(range(img_width)):
                if np.sum(image[ypoint, j]) != 0:
                    xpoint = j
                    x_found_right[idx] = xpoint
                    found = 1
                    break
            ypoint = ypoint + 1

    # initialize an empty array which will be filled with data_point objects
    data_points = np.array([])

    # create the data_point objects for each x-defined point set and add them to the array
    for idx in range(np.alen(x_defined)):
        data_points = np.append(data_points, data_set.data_point(ct.tranform_coordinate([x_defined[idx], y_found_up[idx]], img_height, img_width, cur_location, cur_angle), 1))
        data_points = np.append(data_points, data_set.data_point(ct.tranform_coordinate([x_defined[idx], y_found_down[idx]], img_height, img_width, cur_location, cur_angle), 1))

    # create the data_point objects for each y-defined point set and add them to the array
    for idx in range(np.alen(y_defined)):
        data_points = np.append(data_points, data_set.data_point(ct.tranform_coordinate([x_found_left[idx], y_defined[idx]], img_height, img_width, cur_location, cur_angle), 1))
        data_points = np.append(data_points, data_set.data_point(ct.tranform_coordinate([x_found_right[idx], y_defined[idx]], img_height, img_width, cur_location, cur_angle), 1))

    return data_points
########################################################################################################################






