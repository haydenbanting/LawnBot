'''
Class for bluetooth communication. Note: The RPi hosts the connection and the Android Application becomes a client
of the RPi.

Authors: Hayden Banting, Brett Odaisky
Version: 14  January 2018
'''
########################################################################################################################
from bluetooth import *
import bluetooth
from BluetoothCommunication import constants as const
########################################################################################################################
class BluetoothConnection():

    def __init__(self, uuid=const.DEFAULT_UUID, backlog=const.DEFAULT_BACKLOG):
        '''
        This function is ran once an instance of BluetoothConnection is created. By default it uses a custom UUID
        for connecting to a particular Google Pixel 2 Android device. To connect to a different device create this
        object using that devices UUID. Also be default only one client may be accepted, if you wish to accept more
        adjust backlog accordingly.

        :param uuid: Universally Unique Identifier (128-bit number, string format)
        :param backlog: Number of connections to accept, maximum of 5 (int)
        '''
        # Assign the UUID and number of connections for this connection
        self.uuid = uuid
        self.backlog = backlog
        self.status = const.STATUS_DISCONNECTED

        # Create a bluetooth socket using the rfcomm protocol , and bind the socket to an available port
        self.server_sock = BluetoothSocket(RFCOMM)
        self.server_sock.bind(('', PORT_ANY))

        # Begin listening for connections
        self.server_sock.listen(backlog)
        self.port = self.server_sock.getsockname()[1]

        # Advertise this connection and wait for connection
        bluetooth.advertise_service(self.server_sock, const.DEFAULT_SERVICE_NAME, service_id=uuid,
                                    service_classes=[self.uuid, SERIAL_PORT_CLASS], profiles=[SERIAL_PORT_PROFILE])
        print(const.WAITING_FOR_CONNECTION.format(self.port))

        # Accept a client
        self.client_sock, self.client_info = self.server_sock.accept()
        self.status = const.STATUS_CONNECTED
        print(const.ACCEPTED_CONNECTION + str(self.client_info))

    def read(self):
        '''
        Pretty sketchy. Needs a lot of work. Needs to output some type of usable data so higher level functions can make
        decisions. Also a lot of hardcoding.

        :return:
        '''
        try:
            while True:

                data = self.client_sock.recv(1024)
                if len(data) == 0: break

                print("received [%s]" % data)

        # raise an exception if there was any error
        except IOError:
            self.disconnect()

    def read_command(self):
        try:
            data = self.client_sock.recv(1024)
            if len(data) == 0:
                return None, None
            data_formatted = data.rstrip().split(',')
            print(data_formatted)

            return data_formatted[0], float(data_formatted[1])
        # raise an exception if there was any error
        except IOError:
            self.disconnect()
            
    def write(self, message):
        self.client_sock.send(message.encode())
        #self.server_sock(message.encode())
        
    def disconnect(self):
        '''
        Use this function to end the bluetooth communication.

        :return: None
        '''
        self.client_sock.close()
        self.server_sock.close()
        self.status = const.STATUS_DISCONNECTED
        print(const.DISCONNECTED)
########################################################################################################################
