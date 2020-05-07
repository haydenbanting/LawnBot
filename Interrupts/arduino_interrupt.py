'''
This file contains functions for setting up and using the RPi GPIO to trigger an interrupt on the Arduino
microcomputer.

Author: Hayden Banting
Version: 21 January 2018
'''
########################################################################################################################
import RPi.GPIO as GPIO
import time
from Interrupts import constants
########################################################################################################################
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(constants.INTERRUPT_PIN, GPIO.OUT)
    GPIO.output(constants.INTERRUPT_PIN, 1)

def send_interrupt_trig():
    GPIO.output(constants.INTERRUPT_PIN, 0)
    time.sleep(1e-3)
    GPIO.output(constants.INTERRUPT_PIN, 1)

