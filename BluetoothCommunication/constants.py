'''
A file which contains all the constants and strings related to the bluetooth comms.

Authors: Hayden Banting, Brett Odaisky
Version: 14  January 2018
'''
########################################################################################################################
DEFAULT_UUID = '936DA01F-9ABD-4D9D-80C7-02AF85C822A8'   # Default universal identifier to be advertised
DEFAULT_SERVICE_NAME = 'LawnBot'                        # Service name to be advertised
DEFAULT_BACKLOG = 1                                     # Number of connections to accept
########################################################################################################################
WAITING_FOR_CONNECTION = '[RPi] Waiting for connection on RFCOMM channel {}'  # Waiting for connection print
ACCEPTED_CONNECTION = '[RPi] Accepted connection from '                       # Accepted connection print
DISCONNECTED = 'Disconnected'                                           # Disconnected print
########################################################################################################################
STATUS_CONNECTED = 'connected'
STATUS_DISCONNECTED = 'disconnected'
########################################################################################################################
COMMAND_GO_HOME = 'Go Home'
COMMAND_STOP = 'Stop'
COMMAND_MOVE_FORWARD = 'Forward'
COMMAND_LEFT = 'Left'
COMMAND_RIGHT = 'Right'
COMMAND_BACK = 'Back'
COMMAND_START = 'Start'
COMMAND_MAPS = 'Maps'
COMMAND_NEW_MAP = 'NewMap'
COMMAND_EXISTING_MAP = 'OldMap'
PARAMETER_CLUSTER = "Clusters"
PARAMETER_TOLERANCE = "Tolerance"
PARAMETER_CONTRAST = "Contrast"
PARAMETER_OBSTACLE = "Obstacle"
PARAMETER_BUFFER = "Buffer"
PARAMETER_RESOLUTION = "Resolution"
