'''
Functions perfroming node to node travel with obstacle avoidance

Author: Brett Odaisky, Kristian Melo
Version: 18 Jan 2018
'''
########################################################################################################################
##Imports
########################################################################################################################
from Mapping.mapping_functions import matrix_builder as mBuilder
from Mapping.go_home_funtions import dijkstras as dij
from Mapping.constants import constants as c
import math as m
import numpy as np
########################################################################################################################
def go_home(lawn, x, y, orrientation, movelist, stepsize, sim):

    edges = mBuilder.build_edges_matrix(lawn)

    path = dij.dijkstra(edges, str(np.array([x, y])), str(lawn[0].location))

    x, y, orrientation, movelist, gohomelist = go_home_test(path[1], x, y, orrientation, movelist, stepsize, sim)

    movelist.append(np.array([x, y]))

    return x, y, orrientation, movelist, gohomelist

#this function is called when the bot is stuck in an infinite loop. It will either find a series of moves to fix this or
#decide that the mapping process is done
def seek_next_location(lawn, x, y, orrientation, movelist, stepsize, sim):

    #get edges matrix needed for dijkstras
    edges = mBuilder.build_edges_matrix(lawn)
    shortestpath = [np.inf]
    gohomelist = []

    #convert starting location to a string for use in dijkstras
    start = str(np.array([x, y]))

    #loop through all nodes in our list
    for node in lawn:

        #we are looking for nodes that are type 2 (obstacle free but not traveled to yet).
        if node.type == 2:

            #convert current destination in list to string for dijkstras
            current = str(np.array([node.location[0], node.location[1]]))

            #calculate path to current node with dijkstras
            path = dij.dijkstra(edges, start, current)

            #if the length of the path to the current nodes is shorter than the privous best path calculated in this for
            #loop, make the current path the new best path.
            if type(path) is not float:
                if path[0] < shortestpath[0]:
                    shortestpath = path

    #if dijkstras finds at least one valid path length will be less than infinite
    if shortestpath[0] < np.inf:

        #use the go home algorithm to make the bot travel to our selected nearest node
        x, y, orrientation, movelist, gohomelist = go_home_test(shortestpath[1], x, y, orrientation, movelist, stepsize, sim)

        #return NOTDONE to continue the mapping process yet, and also our new x, y coordinates, and new orrientation
        return c.NOTDONE, x, y, orrientation, gohomelist

    #if the code makes it to this line then there must be no more new nodes to travel to. Return DONE to finish
    return c.DONE, x, y, orrientation, gohomelist


def go_home_test(path, x, y, orrientation, movelist, stepsize, sim):

    list = []
    gohomelist = []

    #loop through the list of path instructions and put them in the form of an array of nparrays for ease of use
    while len(path[1]) == 2:
        list.append(string_to_array(path[0], sim))
        path = path[1]
    list.append(string_to_array(path[0], sim))

    #We must unpack the path instructions in reverse order so this reverses the list again to put it in the right order
    list = list[::-1]

    gohomelist = [orrientation, len(movelist)]

    #loop through the list of moves to the decided destination
    for loc in list:

        if all(loc == list[0]):
            currentx = loc[0]
            currenty = loc[1]

        else:

            nextx = loc[0]
            nexty = loc[1]

            #calculated new orrientation to move to next node
            orrientation = m.degrees(m.atan2(currentx - nextx, nexty - currenty))

            #gohomelist.append(orrientation)

            # update location
            movelist.append(np.array([x, y]))
            x = nextx
            y = nexty

            #gohomelist.append(stepsize)

            currentx = x
            currenty = y

    return x, y, orrientation, movelist, gohomelist


def string_to_array(string, sim):

    string = string.split('[')
    string = string[1].split(']')
    string = string[0].split()

    if sim == 1:
        numarray = np.array([int(string[0]), int(string[1])])
    else:
        numarray = np.array([float(string[0]),float(string[1])])

    return numarray
