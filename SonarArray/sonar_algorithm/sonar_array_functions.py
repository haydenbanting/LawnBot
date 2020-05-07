'''
Functions for obtaining and analyzing sonar data.

Author: Hayden Banting
Version: 22 Feb 2018
'''
########################################################################################################################
import numpy as np
from SonarArray.sonar_algorithm import constants
########################################################################################################################
def analyze_sonar_data(time_measurements, bot_location, bot_angle):
    '''
    This function will analyze the sonar time measurements and compute true obstacle locations with respect to the
    true origin. It considers all geometry, including bot location, bot angle, sonar location, and sonar angle in
    order to represent the obstacle with respect to the true starting origin.

    :param time_measurements: array of time data [np.array or list]
    :param bot_location: location of bot [np.array or list]
    :param bot_angle: current angle of bot in degrees [scalar]
    :return: obstacles: multi-dimensional array where each columnn represents an (x,y) obstacle point
    :return: errors: The worst-case errors associated with each computed obstacle point
    '''

    # Ensure the given number of time measurements is consistent with number of sensors
    assert(len(time_measurements) == len(constants.sonar_positions))

    # Initialize some variables and structures
    obstacles = np.zeros(shape=(1,2))
    errors = []
    sonar_idx = 0


    for ti in time_measurements:

        if ti > 2.0 * constants.dmax / constants.c0:
             #If the time measurement is large, there is not obstacle, skip this data point
            pass

        else:

            # Fetch some information about the current sonar ebing analyzed
            sonar_pos = constants.sonar_positions[sonar_idx]
            sonar_ang = constants.sonar_angles[sonar_idx]

            # Sonar distance calculation from time measurement
            di = constants.c0 * ti / 2

            # Compute obstacle locations
            #xi = (bot_location[0] + sonar_pos[0]) + di * np.cos(sonar_ang * constants.DEG_TO_RAD)
            #yi = (bot_location[1] + sonar_pos[1]) + di * np.sin(sonar_ang * constants.DEG_TO_RAD)
            xi = (sonar_pos[0]) + di * np.cos(sonar_ang * constants.DEG_TO_RAD)
            yi = (sonar_pos[1]) + di * np.sin(sonar_ang * constants.DEG_TO_RAD)

            # Consider the mounting angle of the sonar as well as the current angle of the bot (rotation of plane)
            #xp = (xi * np.cos(bot_angle * constants.DEG_TO_RAD) - yi * np.sin(bot_angle * constants.DEG_TO_RAD))
            #yp = (xi * np.sin(bot_angle * constants.DEG_TO_RAD) + yi * np.cos(bot_angle * constants.DEG_TO_RAD))
            
            xp = (xi * np.cos(bot_angle * constants.DEG_TO_RAD) - yi * np.sin(bot_angle * constants.DEG_TO_RAD)) + bot_location[0]
            yp = (xi * np.sin(bot_angle * constants.DEG_TO_RAD) + yi * np.cos(bot_angle * constants.DEG_TO_RAD)) + bot_location[1]

            #xp = xi
            #yp = yi

            # Compute the errors associated with this data point
            error_x = di * np.sin(constants.alpha * constants.DEG_TO_RAD) + constants.eps_sonar
            error_y = di - di * np.cos(constants.alpha * constants.DEG_TO_RAD) + constants.eps_sonar
            error = np.sqrt(error_x**2 + error_y**2)

            # Update data arrays
            obstacles = np.vstack((obstacles, np.array([xp, yp])))
            errors = np.append(errors, error)

        sonar_idx = sonar_idx + 1

    # Delete meaningless row fom array initialization
    obstacles = np.delete(obstacles, 0, 0)

    return obstacles, errors

########################################################################################################################

