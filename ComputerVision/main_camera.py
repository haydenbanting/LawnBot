'''
Main function for capturing images

Author: Hayden Banting
Version: 05 November 2017
'''
########################################################################################################################
## Imports
########################################################################################################################
import time
import os
from picamera import PiCamera
from ComputerVision.constants import constants as const
from ComputerVision.vision_parameters import performance_parameters as pp
from ComputerVision.vision_parameters import input_parameters as ip
########################################################################################################################
camera = PiCamera()
camera.resolution = pp.RESOLUTION
########################################################################################################################
def capture_image(img_num = 1, cur_location=(0,0), cur_angle=0):
    #camera.start_preview()
    camera.capture(os.path.join(ip.FILEPATH, const.STRING_CAPTURED_IMAGE_FILE.format(img_num, cur_location, cur_angle)))
    #camera.stop_preview()
########################################################################################################################