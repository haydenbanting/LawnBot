'''
Transform image coordinates to relative real cartesian coordinates

Author: Hayden Banting
Version: 22 October 2017
'''
########################################################################################################################
import numpy as np
from ComputerVision.constants import constants as const
from ComputerVision.vision_parameters import performance_parameters as pp
########################################################################################################################
def tranform_coordinate(coor, img_height, img_width, cur_location=[0,0], cur_angle=0):

    # Linear transform and scaling
    #coor[0] = cur_location[0] + pp.METER_PER_PIXEL*(coor[0] - img_width / 2)
    #coor[1] = cur_location[1] + pp.METER_PER_PIXEL*(img_height - coor[1])
    
    cur_angle = cur_angle - 90
    
    coor[0] = pp.METER_PER_PIXEL*(coor[0] - img_width / 2)
    coor[1] = pp.METER_PER_PIXEL*(img_height - coor[1]) + const.CALIBRATION_OFFSET

    # Rotation of the plane
    #xp = coor[0]*np.cos(cur_angle * const.DEG_TO_RAD) - coor[1]*np.sin(cur_angle * const.DEG_TO_RAD)
    #yp = coor[0]*np.sin(cur_angle * const.DEG_TO_RAD) + coor[1]*np.cos(cur_angle * const.DEG_TO_RAD)
    
    xp = coor[0]*np.cos(cur_angle * const.DEG_TO_RAD) - coor[1]*np.sin(cur_angle * const.DEG_TO_RAD) + cur_location[0]
    yp = coor[0]*np.sin(cur_angle * const.DEG_TO_RAD) + coor[1]*np.cos(cur_angle * const.DEG_TO_RAD) + cur_location[1]

    return [xp, yp]
