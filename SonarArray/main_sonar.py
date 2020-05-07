'''
Main script for ssonar sensing script.

Author: Hayden Banting
Version: 28 December 2017
'''
########################################################################################################################
## Imports
import matplotlib.pyplot as plt
import numpy as np
from sonar_algorithm import sonar_array_functions, constants
########################################################################################################################

def test_sonar(time_data):

    #print("Time Data: ", time_data)
    print("Max Time: {}".format(2.0 * constants.dmax / constants.c0))
    ########################################################################################################################
    '''
    If you want to use to script, be sure to comment out everything below and just use the chunks above. Everything
    below is an examples of how to sue and handle the data.
    '''
    # Sample Data
    bot_location = (0,0.0)
    bot_angle = 0

    # Analyze Data
    obstacles, errors = sonar_array_functions.analyze_sonar_data(time_data, bot_location, bot_angle)

    #print(time_data)
    print(obstacles)
    #print(errors)

    # Sample Plot
    plt.figure(1000)
    ax = plt.axes()

    ax.plot(obstacles[:,0], obstacles[:,1], 'o')

    for i in range(len(constants.sonar_positions)):

        #arrow1 = plt.Arrow(constants.sonar_positions[i][0] + bot_location[0], constants.sonar_positions[i][1] + bot_location[1],
                 #0.1 * np.cos((constants.sonar_angles[i] + bot_angle + constants.alpha) * constants.DEG_TO_RAD),
                 #0.1 * np.sin((constants.sonar_angles[i] + bot_angle + constants.alpha) * constants.DEG_TO_RAD), width=0.01)
        #arrow2 = plt.Arrow(constants.sonar_positions[i][0] + bot_location[0], constants.sonar_positions[i][1] + bot_location[1],
                 #0.1 * np.cos((constants.sonar_angles[i] + bot_angle - constants.alpha) * constants.DEG_TO_RAD),
                 #0.1 * np.sin((constants.sonar_angles[i] + bot_angle - constants.alpha) * constants.DEG_TO_RAD), width=0.01)
        
        xi = constants.sonar_positions[i][0] #+ bot_location[0]
        yi = constants.sonar_positions[i][1] #+ bot_location[1]
        
        xp = (xi * np.cos(bot_angle * constants.DEG_TO_RAD) - yi * np.sin(bot_angle * constants.DEG_TO_RAD)) + bot_location[0]
        yp = (xi * np.sin(bot_angle * constants.DEG_TO_RAD) + yi * np.cos(bot_angle * constants.DEG_TO_RAD)) + bot_location[1]
        
        
        ax.plot(xp, yp, 'rx')

       # ax.plot(obstacles[i][0], obstacles[i][1], 'o')

       #circle = plt.Circle(obstacles[i], errors[i], fill=0)
        #ax.add_patch(circle)
        #ax.add_patch(arrow1)
        #ax.add_patch(arrow2)

    #plt.ylim(0+bot_location[1], 3+bot_location[1])
    #plt.xlim(-0.3+bot_location[0], 0.3+bot_location[0])
    plt.title('Response of Sonar Array for a Bot Location of ({},{}) and Bot Angle of {}'.format(bot_location[0],
                                                                                                 bot_location[1],
                                                                                                 bot_angle))
    plt.legend(['Data Points', 'Transmitter Locations'])
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.show()
########################################################################################################################


