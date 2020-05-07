'''
Main script for the Lawn Bot.

Authors: Hayden Banting, Kristian Melo, Brett Odaisky
Version: 9 March 2018

Revision 1.0: (Hayden and Kristian) First integration session which interfaces the serial communication code,
                                    computer vision code, and sonar code with the the basic implementation of the
                                    first pass algorithm. Verified and tested to be working.

Revision 1.1: (Hayden)              Code clean up and documentation. Removed numerous print statements used for testing.

Revision 1.2: (Hayden)              Computer vision data is now understood by the mapping functions and movement
                                    functions can now be accessed based on both computer vision and sonar data.

Revision 1.3: (Hayden)              Added supporting utilizing functions to the mapping software for writing and reading
                                    a numpy.array to/from a binary file. Also added checks to see if first_pass()
                                    should run or not based on if there already exists a previous lawn matrix stored.
                                    Now complicated data structures within numpy.arrays can be saved and re-used on
                                    subsequent runs.

Revision 1.4: (Hayden and Brett)    Implemented a class for basic wireless communication with the GUI. A connection
                                    can be established and the RPi can receive bytes from the Android GUI. Still need
                                    to develop additional software to translate messages received into function calls
                                    and sent messages back to the Android App to let it know the function was completed
                                    successfully. (These additional changes to be done by Brett)

Revision 1.5: (Hayden)              Improved high-level framework of the Lawn Bot main script. Added two possible modes
                                    which are manual and autonomous. In autonomous mode the Lawn Bot will execute
                                    functions on its own and utilize the mapping functions. In manual mode the the Lawn
                                    Bot will only execute functions which it receives from the Android GUI. Also
                                    cleaned and documented the BluetoothCommunication module to be consistent with the
                                    documentation of other modules.

Revision 1.6: (Kristian)            Updated the first pass algorithm code with the newer, more robust version. Added a
                                    setting for selecting between two new modes: simulation and hardware. Simulation
                                    runs the first pass code like the stand alone script. Hardware mode requires the
                                    integration with the sensors and motors. The appropriate calls to functions and
                                    data handeling from the hardware was also added and adjusted to fit with the updated
                                    code. This code has also changed so that once the map has been created, it also
                                    generates instructions to return to the origin.

Revision 1.7: (Hayden and Brett)    Finished development of RPi-side GUI client. Now messages sent by the Android App
                                    are interpreted correctly and the correct functions are excepted.

Revision 1.8: (Hayden)              Added functionality that if a "stop" command is issued by the android app a trigger
                                    is sent from the RPi GPIO to the Arduino GPIO which will issue an ISR on the
                                    Arduino. This functionality is needed as the motors should stop immediately if a
                                    stop command is received.
                                    Also wrote a unix shell script for the RPi. Upon RPi power-up the shell script will
                                    run and the software automatically.

Revision 1.9: (Kristian)            Completed mapping and cutting phases of bot routing. Bot can map a lawn, save the
                                    map to memory. Then, when run again it can take that map in memory, find a cutting
                                    path through the yard and send those instructions to the motors.

Revision 2.0 (All)                  Numerous bug fixes. Integrtation of graphical user interface anf functionality
                                    associated with that. Ready for presentation day.
'''
########################################################################################################################
## Imports
########################################################################################################################
import numpy as np
import threading
import time
import math as m
import sys
import matplotlib.pyplot as plt
from ComputerVision import main_cv as cv
from ComputerVision.constants import constants as cvc
from ComputerVision.vision_parameters import performance_parameters as pp
from SerialCommunication import rpi_side_comms as sc
from BluetoothCommunication import rpi_side_comms as bc
from BluetoothCommunication import constants as bcc
from SonarArray import main_sonar as ms
from SonarArray.sonar_algorithm import sonar_array_functions as sa
from Mapping.constants import constants as c
from Mapping.mapping_functions import collision_detection as cd
from Mapping.mapping_functions import first_pass_processing as fpp
from Mapping.mapping_functions import plotting_functions as plot
from Mapping.go_home_funtions import go_home_processes as ghp
from Mapping.map_utilities import map_memory as mm
from Mapping.mapping_functions import efficient_path_processing as epp
from Interrupts import arduino_interrupt as aint
from PowerManagement import check_discharge as bd
########################################################################################################################
## Parameters
########################################################################################################################
manual = 'manual'           # Whether or not manual control will be used
autonomous = 'autonomous'   # Whether or not autonomous control will be used
arduinoComms = None         # Placeholder for arduino communications object
androidComms = None         # Placeholder for android communications object
TOTAL_COUNT = 38 * 3600     # Global constant which is the total battery coloumb count, used to check discharge
########################################################################################################################
## High Level Functions
########################################################################################################################
def first_pass(lawn=[]):
    '''
    This function executes the first pass mapping phase and builds a matrix of lawn after discovering obstacles. Both
    obstacles and absence of obstacles are included in the map so both areas which need to be traversed and those to
    avoid are known.


    :return: None
    '''

    ##initial conditions
    x = 0.0
    y = 0.0
    movelist = []
    orrientation = c.EAST
    stuck = 0
    done = 0

    # loop until all mapping has been completed
    while not done:

        # loop until obstacles indicate no new valid moves 4 times in a row
        while stuck < 4:

            if c.SIMULATION_MODE:
                # reads obstacles from a text file map for simulations
                obstacles = fpp.check_for_obstacles(x, y, orrientation)

                # update map
                lawn, stuck = fpp.update_map(x, y, obstacles, orrientation, lawn, movelist, stuck)

                # manually change orrientation variable depending on selected direction
                orrientation, turn = fpp.select_direction(obstacles, orrientation)

                #check for obstacles again after turn since the front facing obstacle detection is more precise
                obstacles = fpp.check_for_obstacles(x, y, orrientation)

                #update map
                lawn, stuck = fpp.update_map(x, y, obstacles, orrientation, lawn, movelist, stuck)

                #if we're still sure that the node in front of us is clear, continue with the move
                if obstacles[1] != 9:
                    # manually change location to virtually "move" arround simulated map
                    x, y = fpp.move_bot(orrientation, x, y, turn, c.GRIDSIZE)

            else:
                # reads obstacles from obstacle detection hardware
                obstacles = check_for_obstacles(x, y, orrientation)
                
                print('obstacles from sonar: '+str(obstacles))
                # update map
                lawn, stuck = fpp.update_map(x, y, obstacles, orrientation, lawn, movelist, stuck)
                
                print('obstacles after update' + str(obstacles))

                #select direction and change orrientation variable in memory
                orrientation, turn = fpp.select_direction(obstacles, orrientation)
                
                if turn == c.BACKWARD:
                    arduinoComms.rotate(turn)
                    
                elif turn == c.STRAIGHT:
                    x, y = fpp.move_bot(orrientation, x, y, turn, c.GRIDSIZE)
                    arduinoComms.move_forward(c.GRIDSIZE)
                    
                else:
                        
                    # send the motors turning instructions
                    arduinoComms.rotate(turn)

                    # check for obstacles again after turn since the front facing obstacle detection is more precise
                    obstacles = check_for_obstacles(x, y, orrientation)
                
                    print('obstacles after sonar' + str(obstacles))
                    # update map
                    lawn, stuck = fpp.update_map(x, y, obstacles, orrientation, lawn, movelist, stuck)
                
                    print('obstacles after update' + str(obstacles))

                    # if we're still sure that the node in front of us is clear, continue with the move
                    if obstacles[1] != 9:
                        #change the location in memory
                        x, y = fpp.move_bot(orrientation, x, y, turn, c.GRIDSIZE)

                        #send move command to motors
                        arduinoComms.move_forward(c.GRIDSIZE)
                    
                #check to see if battery is low
                count = arduinoComms.check_battery()
                if bd.check_low_battery(count):
                    print('low battery, going home')
                    stuck = 4
                    done = 1

                # Updates to send Android
                
                # Update battery life
                battery_percent = abs((TOTAL_COUNT - arduinoComms.check_battery())/TOTAL_COUNT*100)
                battery_string = 'Battery:' + '{0:.2f}'.format(battery_percent)
                print('[RPi] Sending to Android: ' + battery_string)
                androidComms.write(battery_string+'\n')

                # Update most recent obstcales seen
                for node in lawn[-3:]:
                    if node.type == 9:
                        obs_string = 'Obstacle:{},{}'.format(node.location[0],node.location[1])
                        print('[RPi] Sending to Android: ' + obs_string)
                        androidComms.write(obs_string+'\n')

                # Update robots current position
                pos_string = 'Position:{},{}'.format(x,y)
                print('[RPi] Sending to Android: ' + pos_string)
                androidComms.write(pos_string+'\n')
                
                #check if propagating error is becoming an issue
                if size(movelist) > 195:
                    print('WARNING: Propagating error may be beyond 30cm.')
                    androidComms.write('WARNING\n')
                    

            #send_map_to_bluetooth(lawn)


        # reset the stuck counter, next function will fix being stuck
        stuck = 0

        # find next valid move, if none we are finished
        done, x, y, orrientation, gohomelist = ghp.seek_next_location(lawn, x, y, orrientation, movelist, c.GRIDSIZE, c.SIMULATION_MODE)

        if c.SIMULATION_MODE != 1:
            exicute_gohomelist(gohomelist)

    '''
    Once this section of code is reached all nodes in the yeard have been discovered and visited. This next section of 
    code generates the directions to take the bot back to the orgin (x, y = 0, 0)
    '''
    print('start go home process')
    
    x, y, orrientation, movelist, gohomelist = ghp.go_home(lawn, x, y, orrientation, movelist, c.GRIDSIZE, c.SIMULATION_MODE)

    if c.SIMULATION_MODE != 1:
        print('Total move list was:')
        print(movelist)
        print('movelist sent to gen movement list:')
        print(movelist[gohomelist[1]:])
        print(gohomelist[0])
        
        gohomelist = fpp.generate_movement_list(movelist[gohomelist[1]:], gohomelist[0], c.GRIDSIZE)
        print('Go home list was:')
        print(gohomelist)
        exicute_gohomelist(gohomelist)

    # plot graph of locations
    #plot.plot_lawn(lawn, movelist)

    # Write the lawn matrix to binary
    lawn.append(c.DONE)
    mm.write_map_to_binary(lawn)


    print("Done map")

########################################################################################################################
def send_map_to_bluetooth(lawn):
    obstacle_string = ''

    for node in lawn:
        if node.type == 9:
            obstacle_string += str(node.location[0]) + ',' + str(node.location[1]) + ';'

    #androidComms.write(obstacle_string)
    print(obstacle_string)

    return obstacle_string
########################################################################################################################
def run_first_pass():

    process = threading.Thread(target=first_pass)
    process.start()

    while process.is_alive():

        command, command_args = androidComms.read_command()

        if command == bcc.COMMAND_STOP:
            process.join()
########################################################################################################################
def check_for_obstacles(x, y, orrientation):
    '''
    This function utilities the sonar sensing functions as well as the computer vision functions to detect nearby
    obstacles. It then feeds the obstacle locations to a function which formats them in a way which @KristianMelo's
    mapping algorithm can better understand.

    :param x: current x-cor
    :param y: current y-cor
    :param orrientation: current orientation (degrees)
    :return: Obstacle data relative to bot (array)
    '''

    # Collect sonar data (Already in understandable format)
    sonar_position, sonar_errors = sa.analyze_sonar_data(arduinoComms.collect_data(), (x,y), orrientation)

    obstacles = np.zeros((3)) + 2

    obstacles = cd.hardware_obsctale_check(x, y, orrientation, sonar_position, obstacles, 1)
    
    if obstacles[1] != 9:
    
        # Call the computer vision algorithm and capture potential obstacle information
        comp_vision_position = cv.main_computer_vision(cur_location=(x, y), cur_angle=orrientation)

        # Transform data into understandable format by mapping functions
        comp_positions = np.zeros(shape=(1, 2))
        for obst in comp_vision_position:
            comp_positions = np.vstack((comp_positions, np.array(obst.location)))
    
        obstalces = cd.hardware_obsctale_check(x, y, orrientation, comp_positions, obstacles, 0)

    return obstacles
########################################################################################################################
def exicute_gohomelist(gohomelist):

    for i in range(len(gohomelist)):
        
        # every odd instruction is a turn.
        #don't perform any move if it is 0
        if gohomelist[i] != 0:
            if i % 2 != 0:
                arduinoComms.rotate(gohomelist[i])
            else:
                arduinoComms.move_forward(gohomelist[i])


    return
########################################################################################################################
def produce_discharge_curve():
    
    TOTAL_COUNT = 38 * 3600
    DEPTH_OF_DISCHAGE_THRESH = 0.5
    TIME_DELAY = 0.1
    MAX_ITERATIONS = 45
    
    start_time = time.time()
    
    count = [(TOTAL_COUNT - arduinoComms.check_battery())/TOTAL_COUNT*100]
    t = [0]
    i = 0
    
    while count > TOTAL_COUNT * DEPTH_OF_DISCHAGE_THRESH and i < MAX_ITERATIONS:
        
        arduinoComms.move_forward(0.62831)
        
        new_count = (TOTAL_COUNT - arduinoComms.check_battery())/TOTAL_COUNT*100
        new_time = time.time() - start_time
        
        print('Count at {}s is: {}'.format(new_time, new_count))
        
        t.append(new_time)
        count.append(new_count)
        
        i += 1
        
        time.sleep(TIME_DELAY)
        
    plt.figure(10000)
    plt.plot(t, count)
    plt.title('Discharge Curve')
    plt.xlabel('Time [s]')
    plt.ylabel('Depth of Discharge [%]')
    plt.show()
########################################################################################################################
## Main Script Set-up
mode = 'autonomous'
#mode = 'manual'

# Set up serial connection with Arduino
arduinoComms = sc.SerialConnection()
arduinoComms.read()

# Set up wireless bluetooth connection with Android
androidComms = bc.BluetoothConnection()


wait_for_start = 1
wait_for_routine = 1
new_map = 1
existing_map = 0


while wait_for_start:
    
    command, command_args = androidComms.read_command()
    #print('[RPi] Received command from Android: ' + command)
    #androidComms.write('Received command: ' + command)
    
    if command == bcc.COMMAND_START:
        
        wait_for_start = 0
        

while wait_for_routine:
    
    command, command_args = androidComms.read_command()
    
    if command == bcc.COMMAND_NEW_MAP:
        
        new_map = 1
        wait_for_routine = 0

    elif command == bcc.COMMAND_EXISTING_MAP:
        
        existing_map = 1
        wait_for_routine = 0
    

########################################################################################################################
## Autonomous Mode
########################################################################################################################
if mode == autonomous:

    print('[RPi] Starting autonomous Lawn Bot control.')

    # Start cutting
    if (mm.check_for_binary_map() == []) or new_map: # Either starting a new lawn or no old lawn found
        starttime = time.time()
        print('[RPi] Starting first pass.')
        first_pass()
        endtime = time.time()
        print((endtime - starttime))

    else: # Found an old lawn
        lawn = mm.get_most_recent_map()

        #run optimized on routine from old first pass
        if lawn[len(lawn)-1] == c.DONE:
            print('[RPi] Found a known completed lawn. Computing optimized routine.')
            lawn = np.delete(lawn, len(lawn)-1)
            movelist = epp.efficient_path(lawn)

            instructions = fpp.generate_movement_list(movelist, c.EAST)

            print(instructions)

            if c.SIMULATION_MODE != 1:
                exicute_gohomelist(instructions)

        # Never finished first pass, resume
        else:
            print('[RPi] Found a known incompleted lawn. Resuming mapping routine.')

            lawn = mm.get_most_recent_map()

            first_pass(lawn)


########################################################################################################################
## Manual Mode
########################################################################################################################
if mode == manual:

    print('[RPi] Starting manual Lawn Bot control.')
    print('[RPi] Waiting for commands from the Android application...')

    while androidComms.status == bcc.STATUS_CONNECTED:

        # Next command in queue from Android (function doesn't exist)
        command, command_args = androidComms.read_command()

        if command == bcc.COMMAND_STOP:
            #aint.send_interrupt_trig()
            print('[RPi] Sent trigger...')

        if command == bcc.COMMAND_MOVE_FORWARD:
            arduinoComms.move_forward(command_args)

        if command == bcc.COMMAND_LEFT:
            arduinoComms.rotate(90)

        if command == bcc.COMMAND_RIGHT:
            arduinoComms.rotate(-90)

        if command == bcc.COMMAND_BACK:
            arduinoComms.rotate(180)

        if command == bcc.PARAMETER_BUFFER:
            pp.BUFFER = command_args

        if command == bcc.PARAMETER_CLUSTER:
            pp.N_CLUSTERS = command_args

        if command == bcc.PARAMETER_CONTRAST:
            pp.CONTRAST_THRESHOLD = command_args

        if command == bcc.PARAMETER_OBSTACLE:
            pp.SMALL_OBSTACLE = command_args

        if command == bcc.PARAMETER_RESOLUTION:
            pp.RESOLUTION = command_args

        if command == bcc.PARAMETER_TOLERANCE:
            pp.TOL = command_args


########################################################################################################################
# Finished
########################################################################################################################
print('Finished')

