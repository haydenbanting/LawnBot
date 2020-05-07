
'''
A file for all the constants relevant to the serial communication.

Author: Hayden Banting
Version: 28 December 2017
'''
########################################################################################################################
PORT = '/dev/ttyACM0'   # Port on RPi where a port is attempted to be opened
BAUDRATE = 9600         # Baud rate of the port
COMMS_DELAY = 1e-6      # A short time delay to wait for other controller to respond
MICRO = 1e-6            # FOr converting between microseconds and seconds
########################################################################################################################
LOG_HELLO = '[RPi] Saying hello to the arduino...'  # Log message is user wants to track communication
LOG_SENDING_COMMAND = '[RPi] Sending command to arduino...'    # Log message is user wants to track communication
########################################################################################################################
COMMAND_HELLO = "Hello from RPi\n"  # String format of handshake
COMMAND_MOVE = "CMD_FORWARD: {}\n"  # String format of move command (takes 1 argument when formatting)
COMMAND_ROTATE = "CMD_ROTATE: {}\n" # String format of rotate command (takes 1 argument when formatting)
COMMAND_COLLECT = "CMD_COLLECT\n"   # String format of collect sonar data command
COMMAND_BATTERY = "CMD_BATTERY\n"   # String fomrat of check battery life command
RESPONSE_DELIMITER = ":"            # Character to split message by
########################################################################################################################
