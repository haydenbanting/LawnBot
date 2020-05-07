'''
Functions to calculated a cutting path through a known lawn

Author: Kristian Melo
Version: 29 Jan 2018
'''
########################################################################################################################
##Imports
########################################################################################################################
from Mapping.constants import constants as c
from Mapping.map_utilities import map_memory as mm
from Mapping.mapping_functions import first_pass_processing as fpp
from Mapping.go_home_funtions import  go_home_processes as ghp
from Mapping.mapping_functions import plotting_functions as plot
import numpy as np
import matplotlib.pyplot as plt
import math as m
import pylab
########################################################################################################################

#same class as 'Node' using in mapping phase
class Cutting_Node(object):

    def __init__(self, location, type, neighbors=[]):
        self.location = location
        self.type = type
        self.neighbors = neighbors

    #updates neighbors of a node insuring no duplicates
    def update_neighbor(self, loc):
        if len(self.neighbors) == 0:
            self.neighbors.append(loc.astype(np.float64))
        repeat = 0
        for i in self.neighbors:
            if all(loc == i):
                repeat += 1
                break
        if repeat == 0:
            self.neighbors.append(loc.astype(np.float64))

########################################################################################################################

#generate list of movements to be stored that can be followed to cut the lawn
def efficient_path(lawn):

    #perform nodal array transform.
    tspnodes = place_tsp_nodes_half(lawn)

    x = tspnodes[0].location[0]
    y = tspnodes[0].location[1]
    movelist = []
    orrientation = c.NORTH
    stuck = 0
    done = 0

    # loop until all mapping has been completed
    while not done:

        # loop until obstacles indicate no new valid moves 4 times in a row
        while stuck < 4:

                # reads obstacles from a text file map for simulations
                obstacles = get_obstacles(x, y, orrientation, tspnodes)

                # update map
                tspnodes, stuck = update_map(x, y, obstacles, orrientation, tspnodes, movelist, stuck)

                # manually change orrientation variable depending on selected direction
                orrientation, turn = select_direction(obstacles, orrientation)

                # manually change location to virtually "move" arround simulated map
                x, y = fpp.move_bot(orrientation, x, y, turn, c.RADIUS)

        # reset the stuck counter, next function will fix being stuck
        stuck = 0

        # find next valid move, if none we are finished
        done, x, y, orrientation, gohomelist = ghp.seek_next_location(tspnodes, x, y, orrientation, movelist, c.RADIUS, 0)

    '''
    Once this section of code is reached all nodes in the yeard have been discovered and visited. This next section of
    code generates the directions to take the bot back to the orgin (x, y = 0, 0)
    '''

    x, y, orrientation, movelist, gohomelist = ghp.go_home(tspnodes, x, y, orrientation, movelist, c.RADIUS, 0)

    # plot graph of locations
    #plot.plot_lawn(tspnodes, movelist)

    # Write the lawn matrix to binary
    #mm.write_map_to_binary(movelist)

    return movelist

########################################################################################################################

'''
Transforming the nodal array is a key portion to start creating the cutting route. In the mapping phase our gridsize
was dependant by the physical size of the entire bot. For cutting though, our gridsize has to be relitive to the size of
the mowing blade that could fit under the bot. This is to ensure that visiting every node equates to cutting all the
grass. So we must take our larger nodes we achieve while mapping and place extra nodes around these to ensure full
coverage. I have arranged the nodes in a square grid formation with no overlap. Although this leaves spaces between
nodes you can see later that the way the bot will travel ensures that this empty space will be covered via transitions.
'''
def place_tsp_nodes_half(lawn):
    tspnodes = []

    #add all nodes from lawn into tspnodes. Additionally, add nodes between these nodes with proper type classification
    for node in lawn:

        if node.type != 9:
            tspnodes.append(Cutting_Node(node.location.astype(np.float64), 2, []))

            nodepos = len(tspnodes) - 1

            for node2 in lawn:

                if node2.type != 9:

                    if node.location[0] + c.GRIDSIZE == node2.location[0] and node.location[1] == node2.location[1]:
                        tspnodes = add_tsp_node(tspnodes, node, node2, c.RADIUS, 0, nodepos)
                    elif node.location[0] - c.GRIDSIZE == node2.location[0] and node.location[1] == node2.location[1]:
                        tspnodes = add_tsp_node(tspnodes, node, node2, -c.RADIUS, 0, nodepos)
                    elif node.location[0] == node2.location[0] and node.location[1] + c.GRIDSIZE == node2.location[1]:
                        tspnodes = add_tsp_node(tspnodes, node, node2, 0, c.RADIUS, nodepos)
                    elif node.location[0] == node2.location[0] and node.location[1] - c.GRIDSIZE == node2.location[1]:
                        tspnodes = add_tsp_node(tspnodes, node, node2, 0, -c.RADIUS, nodepos)

        else:
            tspnodes.append(Cutting_Node(node.location.astype(np.float64), 9, []))

            off1, off2, off3, off4 = 1,1,1,1
            for node2 in lawn:
                if node2.type == 3:
                    if node.location[0] + c.GRIDSIZE == node2.location[0] and node.location[1] == node2.location[1]:
                        off1 = 0
                    elif node.location[0] - c.GRIDSIZE == node2.location[0] and node.location[1] == node2.location[1]:
                        off2 = 0
                    elif node.location[0] == node2.location[0] and node.location[1] + c.GRIDSIZE == node2.location[1]:
                        off3 = 0
                    elif node.location[0] == node2.location[0] and node.location[1] - c.GRIDSIZE == node2.location[1]:
                        off4 = 0

            if off1 == 1:
                tspnodes, pos = update_node(tspnodes, np.array([node.location[0] + c.RADIUS, node.location[1]]), 9)
            if off2 == 1:
                tspnodes, pos = update_node(tspnodes, np.array([node.location[0] - c.RADIUS, node.location[1]]), 9)
            if off3 == 1:
                tspnodes, pos = update_node(tspnodes, np.array([node.location[0], node.location[1] + c.RADIUS]), 9)
            if off4 == 1:
                tspnodes, pos = update_node(tspnodes, np.array([node.location[0], node.location[1] - c.RADIUS]), 9)

    #there is still blank spaces between some nodes. Loop through the ones without 4 'neighbores' and add more nodes
    #in these gaps
    nodepos = 0
    for node in tspnodes:

        if len(node.neighbors) < 4 and node.type == 2:

            for node2 in tspnodes:

                if node2.type == 2 and len(node2.neighbors) < 4:

                    if node.location[0] + c.GRIDSIZE == node2.location[0] and node.location[1] == node2.location[1]:
                        tspnodes = add_tsp_node(tspnodes, node, node2, c.RADIUS, 0, nodepos)
                    elif node.location[0] - c.GRIDSIZE == node2.location[0] and node.location[1] == node2.location[1]:
                        tspnodes = add_tsp_node(tspnodes, node, node2, -c.RADIUS, 0, nodepos)
                    elif node.location[0] == node2.location[0] and node.location[1] + c.GRIDSIZE == node2.location[1]:
                        tspnodes = add_tsp_node(tspnodes, node, node2, 0, c.RADIUS, nodepos)
                    elif node.location[0] == node2.location[0] and node.location[1] - c.GRIDSIZE == node2.location[1]:
                        tspnodes = add_tsp_node(tspnodes, node, node2, 0, -c.RADIUS, nodepos)

        nodepos += 1


    return tspnodes

#adds new nodes and neighbors to the node
def add_tsp_node(tspnodes, node, node2, xoff, yoff, nodepos):

    loc = np.array([node.location[0] + xoff, node.location[1] + yoff])
    loc = loc.astype(np.float64)

    tspnodes, pos = update_node(tspnodes, loc, 2)

    tspnodes[nodepos].update_neighbor(loc)

    tspnodes[pos].update_neighbor(node.location)

    return tspnodes


#update a given node with the most relavent information. Also insures no duplicates
def update_node(tspnodes, loc, type):
    pos = 0
    loc = loc.astype(np.float64)

    for node in tspnodes:
        if all(node.location == loc):
            return tspnodes, pos

        pos += 1

    tspnodes.append(Cutting_Node(loc, type, []))

    pos = len(tspnodes) - 1

    return tspnodes, pos



########################################################################################################################

#check memory to see if obstacles are in our next moveset
def get_obstacles(x, y, orrientation, tspnodes):

    obstacles = np.zeros((3)) + 9
    node_x = np.array([-c.RADIUS, 0, c.RADIUS])
    node_y = np.array([0, c.RADIUS, 0])

    #rotate orrientation to do calculations wrt north
    if orrientation == c.NORTH:
        node_x = node_x
        node_y = node_y

    elif orrientation == c.EAST:
        tempx = node_x
        tempy = node_y
        node_x = tempy
        node_y = -1 * tempx

    elif orrientation == c.SOUTH:
        node_x = -1 * node_x
        node_y = -1 * node_y

    else:
        tempx = node_x
        tempy = node_y
        node_x = -1 * tempy
        node_y = tempx

    node_x += x
    node_y += y
    count = 0

    #loop through list of nodes to find nodes and their types at our next move locations
    for node in tspnodes:
        if node_x[0] == node.location[0] and node_y[0] == node.location[1]:
            obstacles[0] =  node.type
            count += 1
            if count == 3:
                break

        elif node_x[1] == node.location[0] and node_y[1] == node.location[1]:
            obstacles[1] =  node.type
            count += 1
            if count == 3:
                break

        elif node_x[2] == node.location[0] and node_y[2] == node.location[1]:
            obstacles[2] =  node.type
            count += 1
            if count == 3:
                break

    #return array of found obstacles
    return obstacles

#selects which direction to turn based on information in the obstacles array
def select_direction(obstacles, orrientation):
    '''
    This block of 'if' statements perform the logic of this funciton. Instead of prioritizing left, straigh, then right
    to traverse the perimeter, we have two sets of logic. If we are facing north or south we prioritize turns. If we are
    facing east or west, we prioritize straigh movement. This causes us to travel through entire horizontal rows at a
    time. This is important because of the nodal array we selected. To ensure we 'mow' the gaps between nodes we must
    exit nodes through the opposite side we came in. This row-wise movemtn allows us to do just that, with the exception
    of corners and edges by obstacles.
    '''

    if orrientation == c.SOUTH or orrientation == c.NORTH:

        if obstacles[0] == 2:
            turn = c.LEFT
        elif obstacles[2] == 2:
            turn = c.RIGHT
        elif obstacles[1] == 2:
            turn = c.STRAIGHT

        elif obstacles[0] == 3:
            turn = c.LEFT
        elif obstacles[2] == 3:
            turn = c.RIGHT
        elif obstacles[1] == 3:
            turn = c.STRAIGHT

        else:
            turn = c.BACKWARD

    elif orrientation == c.EAST or orrientation == c.WEST:

        if obstacles[1] == 2:
            turn = c.STRAIGHT
        elif obstacles[0] == 2:
            turn = c.LEFT
        elif obstacles[2] == 2:
            turn = c.RIGHT

        elif obstacles[1] == 3:
            turn = c.STRAIGHT
        elif obstacles[0] == 3:
            turn = c.LEFT
        elif obstacles[2] == 3:
            turn = c.RIGHT

        else:
            turn = c.BACKWARD

    #the turn we select is added to our orrientation. Both are in units of degrees so they can simply be summed.
    orrientation += turn

    #since our direction constants are simply constants they cannot contain values for all 2*pi. So if our orrientation
    #goes 2*pi above or below some of our constants we reset them to said constant here.
    if orrientation == 270:
        orrientation = c.EAST
    elif orrientation == 360:
        orrientation = c.NORTH
    elif orrientation == -180:
        orrientation = c.SOUTH

    #simply output directions via text for testing purposes
    if turn == c.LEFT:
        print("Turn left")
    elif turn == c.STRAIGHT:
        print("Go straight")
    elif turn == c.RIGHT:
        print("Turn right")
    elif turn == c.BACKWARD:
        print("Turn around")

    return orrientation, turn

def update_map(x, y, obstacles, orrientation, tspnodes, movelist, stuck):

    #set node at current location to type 3 to say that we have visited it.
    for node in tspnodes:
        if all(np.array([x, y]) == node.location):
            node.type = 3
            break

    #add to movelist
    movelist.append(np.array([x, y]))

    #check if we have any valid moves, if not, increment stuck counter
    if all(obstacles != 2):
        stuck += 1
    else:
        stuck = 0

    return tspnodes, stuck