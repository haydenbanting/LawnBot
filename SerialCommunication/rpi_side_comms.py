'''
Class for serial communication.

Note: It doesn't matter which script runs first (Arduino or RPi side), they will wait for each other. However, if a
physical disconnection of the USB cable needs to be made re-run after re-connecting them.

Author: Hayden Banting
Version: 27 January 2018
'''
########################################################################################################################
## Imports
########################################################################################################################
import serial
import time
from SerialCommunication import constants
########################################################################################################################
class SerialConnection():
    '''
    This class contains all information and functions surrounding the arudio-pi serial communication. Upon object
    creation the connection is established, and the user can then send commands and get data whenever necessary through
    the object.
    '''
    def __init__(self, port=constants.PORT, baudrate=constants.BAUDRATE, print_comms=1):
        '''
        This function is the "constructor" of serial communication object, and is ran once upon object creation. It
        establishes the serial connection and sets up some object variables.

        :param port: port to connect to
        :param baudrate: baud rate of connection
        :param print_comms: whether or not to print the communication messages
        '''
        self.ser = serial.Serial(port, baudrate)
        self.ser.baudrate = baudrate
        self.print_comms = print_comms
        self.ser.flushInput()
        self.ser.flushOutput()

        response = self.ser.readline().rstrip()

        if self.print_comms:
            print(response)

        if self.print_comms:
            print(constants.LOG_HELLO)

        self.ser.write(constants.COMMAND_HELLO)
        time.sleep(constants.COMMS_DELAY)

        response = self.ser.readline().rstrip()

        if self.print_comms:
            print(response)

    def collect_data(self):
        '''
        This function issues a collect data command to the arduino. It then processes the response and creates
        an array of time data form the sonar sensors, where the first data is from the first sonar, the second data is
        from the second sonar, and so on.

        :return: Time data array (seconds)
        '''

        if self.print_comms:
            print(constants.LOG_SENDING_COMMAND + constants.COMMAND_COLLECT)

        self.ser.write(constants.COMMAND_COLLECT)
        time.sleep(constants.COMMS_DELAY)
        data = self.ser.readline().rstrip()

        # Split the data into in a list, where each data is seperated by a delimiter
        data = data.split(constants.RESPONSE_DELIMITER)

        # Create a new list of data where entries are floats, not strings, scaled to seconds
        data = [constants.MICRO * float(idata) for idata in data]

        return data

    def move_forward(self, distance):
        '''
        This function issues a move command to the arduino. It waits until the arduio has completed the move.

        :param distance: distance to move (float)
        :return: None
        '''

        if self.print_comms:
            print(constants.LOG_SENDING_COMMAND)

        self.ser.write(constants.COMMAND_MOVE.format(distance))
        time.sleep(constants.COMMS_DELAY)

        response = self.ser.readline().rstrip()

        if self.print_comms:
            print(response)

    def rotate(self, angle):
        '''
        This function issues a rotate command to the arduino. It waits until the arduio has completed the move.

        :param angle: angle to rotate (degrees)
        :return: None
        '''

        if self.print_comms:
            print(constants.LOG_SENDING_COMMAND)

        self.ser.write(constants.COMMAND_ROTATE.format(angle))
        time.sleep(constants.COMMS_DELAY)

        response = self.ser.readline().rstrip()

        if self.print_comms:
            print(response)

    def check_battery(self):

        if self.print_comms:
            print(constants.LOG_SENDING_COMMAND)

        self.ser.write(constants.COMMAND_BATTERY)
        time.sleep(constants.COMMS_DELAY)

        response = self.ser.readline().rstrip()

        if self.print_comms:
            print('[Mega] Coloumb Count:'+ response)

        battery_life = float(response)
        return abs(battery_life)




    def read(self):
        time.sleep(5*constants.COMMS_DELAY)
        response = self.ser.readline().rstrip()

        if self.print_comms:
            print(response)
########################################################################################################################