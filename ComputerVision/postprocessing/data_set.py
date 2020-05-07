'''
Definition of the data_point obstacle and supporting/convenience functions for handling large sets of these objects.

Author: Hayden Banting
Version: 22 October 2017
'''
########################################################################################################################
import matplotlib.pyplot as plt
import numpy as np
from ComputerVision.vision_parameters import output_parameters as op
from ComputerVision.vision_parameters import performance_parameters as pp
from ComputerVision.constants import constants as const
########################################################################################################################
class data_point:
    '''
    This class is used to represent information that the computer vision will output.
    '''
    def __init__(self, location, obstacle):
        '''
        This function is automatically executed upon obstacle creation.

        :param location: x,y coordinates of the data point [tuple]
        :param obstacle: whether or not the data point represents an obstcale point
        '''
        self.location = location
        self.obstacle = obstacle
########################################################################################################################
def plot_data_set(data_set, img_height, img_width, cur_location, cur_angle, fig_num=2, title=op.NODAL_OBSTACLE_TITLE):
    '''
    This function is used for plotting a set of data_point objects.

    :param data_set: an array of data_point objects
    :param fig_num: desired figure number (if creating multiple plots
    '''

    xlower = -0.5*img_width*pp.METER_PER_PIXEL + cur_location[0]
    xupper = 0.5*img_width*pp.METER_PER_PIXEL + cur_location[0]
    ylower = cur_location[1]
    yupper = cur_location[1] + img_height*pp.METER_PER_PIXEL

    xlp = xlower * np.cos(cur_angle * const.DEG_TO_RAD) - ylower * np.sin(cur_angle * const.DEG_TO_RAD)
    xup = xupper * np.cos(cur_angle * const.DEG_TO_RAD) - yupper * np.sin(cur_angle * const.DEG_TO_RAD)
    ylp = xlower * np.sin(cur_angle * const.DEG_TO_RAD) + ylower * np.cos(cur_angle * const.DEG_TO_RAD)
    yup = xupper * np.sin(cur_angle * const.DEG_TO_RAD) + yupper * np.cos(cur_angle * const.DEG_TO_RAD)

    plt.figure(fig_num)
    for data in data_set:
        if data.obstacle:
            plt.scatter(data.location[0], data.location[1], c='r')
            plt.title(title)
            plt.xlabel(op.POS_XLABEL)
            plt.ylabel(op.POS_YLABEL)
            #plt.axis([xlp, xup, ylp, yup])
            #plt.axis([xlower, xupper, ylower, yupper])

########################################################################################################################