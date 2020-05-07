'''
Example usage for serial communication with arduino.

Author: Hayden Banting
Version: 28 December 2017
'''
########################################################################################################################
from SerialCommunication import rpi_side_comms

# Set-up Arduino Comms Channel
arduinoComms = rpi_side_comms.SerialConnection()

# Collect sonar data
time_data = arduinoComms.collect_data()

# Move forward 5.3 meters
arduinoComms.move_forward(5.3)

# Rotate the bot 17.8 degrees
arduinoComms.rotate(17.8)

