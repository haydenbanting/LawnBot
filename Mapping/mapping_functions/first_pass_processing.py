'''
Functions for simulated data

Author: Kristian Melo
Version: 18 Jan 2018
'''
########################################################################################################################
##Imports
########################################################################################################################
import numpy as np
import math as m
from Mapping.constants import constants as c
########################################################################################################################
#Lawn can be viewed as a large grid where each square in the grid is a 'node'. Nodes are created as the bot moves.
class Node(object):
    '''
    Each node has a unique location (nparray) which makes them easily distinguishable.
    Each node also has a type (int) that lets us know whether it is an obstacle, an empty space or a previously visted
    space.
    Each node also has a list of neighbores (array(nparray)) that starts empty and is filled as more neighbores are d
    iscovered.
    '''
    def __init__(self, type, location, neighbors=[]):
        self.type = type
        self.location = location
        self.neighbors = neighbors

    #Adds newly discovered neighbores to a given nodes neighbore list
    def update_neighbor(self, loc):
        if len(self.neighbors) == 0:
            self.neighbors.append(loc)
        repeat = 0
        for i in self.neighbors:
            if all(loc == i):
                repeat += 1
                break
        if repeat == 0:
            self.neighbors.append(loc)

########################################################################################################################
#checks for obstacles in simulated map and returns array of nearby obstacles
def check_for_obstacles(x, y, orrientation):

    #x and y are offset since we set our origin at 0,0 but that may not be where we want to start in a simulated map
    x += c.XOFFSET
    y = c.YOFFSET - y

    x = int(x)
    y = int(y)

    #create empty array to store obstacle data in
    obstacles = np.zeros((3))

    #call function to turn map text file into an array
    testmap = read_file()

    #depending on the bots orrientation we will need to to update different locations relative to the bot.
    #obstacles will always be directly to the left, in front, and the right of the bots current orrientation.
    #obstacle will read '9' for an obstacle or '2' otherwise
    if orrientation == c.NORTH:
        obstacles[0] = testmap[y][x - 1]
        obstacles[1] = testmap[y - 1][x]
        obstacles[2] = testmap[y][x + 1]
    elif orrientation == c.EAST:
        obstacles[0] = testmap[y - 1][x]
        obstacles[1] = testmap[y][x + 1]
        obstacles[2] = testmap[y + 1][x]
    elif orrientation == c.SOUTH:
        obstacles[0] = testmap[y][x + 1]
        obstacles[1] = testmap[y + 1][x]
        obstacles[2] = testmap[y][x - 1]
    else:
        obstacles[0] = testmap[y + 1][x]
        obstacles[1] = testmap[y][x - 1]
        obstacles[2] = testmap[y - 1][x]

    return obstacles


#Turns text file of a simulated lawn shape and puts it into an array for testing
def read_file():
    with open(c.lawnmap) as f:
        testmap = []
        for line in f:
            line = line.split()  # to deal with blank
            if line:  # lines (ie skip them)
                line = [int(i) for i in line]
                testmap.append(line)
    return testmap

########################################################################################################################
#update our array lawn with new nodes and information.
def update_map(x, y, obstacles, orrientation, lawn, movelist, stuck):

    #update node at our current x, y location
    i = update_node(np.array([x, y]), np.array([3]), 0, lawn)

    #update list with current location to keep track of all moves in order
    movelist.append(np.array([x, y]))

    #update information pretaining to surounding nodes. This information changes based on orrientation and for each
    #obstacle.
    if orrientation == c.NORTH:
        #update the node for obstacle 0
        j = update_node(np.array([x - c.GRIDSIZE, y]), obstacles, 0, lawn)
        if obstacles[0] != 9:
            #if this node is not an obstacles make it a valid neighbore of our current location
            lawn[i].update_neighbor(np.array([x - c.GRIDSIZE, y]))
            #if this node is not an obstacle make our current location a valid neighbore of this node
            lawn[j].update_neighbor(lawn[i].location)

        #repeat for other obstacles in obstacle list
        j = update_node(np.array([x, y + c.GRIDSIZE]), obstacles, 1, lawn)
        if obstacles[1] != 9:
            lawn[i].update_neighbor(np.array([x, y + c.GRIDSIZE]))
            lawn[j].update_neighbor(lawn[i].location)

        j = update_node(np.array([x + c.GRIDSIZE, y]), obstacles, 2, lawn)
        if obstacles[2] != 9:
            lawn[i].update_neighbor(np.array([x + c.GRIDSIZE, y]))
            lawn[j].update_neighbor(lawn[i].location)

    #repeat process for all other orrientations
    elif orrientation == c.EAST:
        j = update_node(np.array([x, y + c.GRIDSIZE]), obstacles, 0, lawn)
        if obstacles[0] != 9:
            lawn[i].update_neighbor(np.array([x, y + c.GRIDSIZE]))
            lawn[j].update_neighbor(lawn[i].location)

        j = update_node(np.array([x + c.GRIDSIZE, y]), obstacles, 1, lawn)
        if obstacles[1] != 9:
            lawn[i].update_neighbor(np.array([x + c.GRIDSIZE, y]))
            lawn[j].update_neighbor(lawn[i].location)

        j = update_node(np.array([x, y - c.GRIDSIZE]), obstacles, 2, lawn)
        if obstacles[2] != 9:
            lawn[i].update_neighbor(np.array([x, y - c.GRIDSIZE]))
            lawn[j].update_neighbor(lawn[i].location)

    elif orrientation == c.SOUTH:
        j = update_node(np.array([x + c.GRIDSIZE, y]), obstacles, 0, lawn)
        if obstacles[0] != 9:
            lawn[i].update_neighbor(np.array([x + c.GRIDSIZE, y]))
            lawn[j].update_neighbor(lawn[i].location)

        j = update_node(np.array([x, y - c.GRIDSIZE]), obstacles, 1, lawn)
        if obstacles[1] != 9:
            lawn[i].update_neighbor(np.array([x, y - c.GRIDSIZE]))
            lawn[j].update_neighbor(lawn[i].location)

        j = update_node(np.array([x - c.GRIDSIZE, y]), obstacles, 2, lawn)
        if obstacles[2] != 9:
            lawn[i].update_neighbor(np.array([x - c.GRIDSIZE, y]))
            lawn[j].update_neighbor(lawn[i].location)

    elif orrientation == c.WEST:
        j = update_node(np.array([x, y - c.GRIDSIZE]), obstacles, 0, lawn)
        if obstacles[0] != 9:
            lawn[i].update_neighbor(np.array([x, y - c.GRIDSIZE]))
            lawn[j].update_neighbor(lawn[i].location)

        j = update_node(np.array([x - c.GRIDSIZE, y]), obstacles, 1, lawn)
        if obstacles[1] != 9:
            lawn[i].update_neighbor(np.array([x - c.GRIDSIZE, y]))
            lawn[j].update_neighbor(lawn[i].location)

        j = update_node(np.array([x, y + c.GRIDSIZE]), obstacles, 2, lawn)
        if obstacles[2] != 9:
            lawn[i].update_neighbor(np.array([x, y + c.GRIDSIZE]))
            lawn[j].update_neighbor(lawn[i].location)

    '''
    Some shapes of lawns may result with the bot moving in an infinate loop. To prevent this every time we update the
    list of nodes we check if we have any "new" moves. A new move being an adjacent node that is not an obstacle, and
    also one we havn't traveled to before. If there are no new moves we increment a counter called stuck. If stuck
    increments 4 times in a row it will break a while loop condition in the main script, excicuting some code which will
    find a more appropriate move.
    '''
    if all(obstacles != 2):
        stuck += 1
    else:
        stuck = 0

    return lawn, stuck


#update a given node with the most relavent information
def update_node(loc, obstacles, i, lawn):
    pos = 0

    #search entire list of nodes to see if a node for a given location already exists
    for node in lawn:
        if all(node.location == loc):
            #if the given node already exists update the 'type' of the node with the most important data type
            node.type = update_point(node.type, obstacles[i])

            #Also change the obstacle type with the newly updated node type.
            obstacles[i] = node.type

            #return the possition of the node in the list
            return pos
        pos += 1

    #if a node is not found, then one must not exist for that location, so create a new one
    lawn.append(Node(obstacles[i], loc, []))
    pos = len(lawn) - 1

    return pos


def update_point(old, new):
    '''
    This funciton will take two integer points and return the great one. This is so i can convieniently change data
    types. For example, If i previously saw a node with no obstacle, it would have recieve the type '2'. However later
    we might travel to that node. A node we travel on should recieve the type '3'. So when I update that nodes type
    parameter, this function will replace the previous '2' with the new '3'. Also this does not work the other way so
    that a visited node with value '3' will not be overwitten with a value of '2'
    '''
    if new < old:
        new = old

    return new


########################################################################################################################
#selects which direction to turn based on information in the obstacles array
def select_direction(obstacles, orrientation):
    '''
    This block of 'if' statements perform the logic of this funciton. First we prioritize turning left, straight, and
    right in that order. So first we check if the obstacles in those 3 directions are exclusively of the type 'obstacle
    free'. If all three of these statements are not selected that must mean the only places we can turn are either
    obstacles or places we've been before. So the next three if statements check if our 3 main directions are
    exclusively nodes we've been to before. If all of these are not selected either, it must mean the only places we can
    turn are nodes with obstacles. So finally if this happens we then just tell the bot to turn around.
    '''
    if obstacles[0] == 2:
        turn = c.LEFT
    elif obstacles[1] == 2:
        turn = c.STRAIGHT
    elif obstacles[2] == 2:
        turn = c.RIGHT
    elif obstacles[0] == 3:
        turn = c.LEFT
    elif obstacles[1] == 3:
        turn = c.STRAIGHT
    elif obstacles[2] == 3:
        turn = c.RIGHT
    else:
        turn = c.BACKWARD

    #the turn we select is added to our orrientation. Both are in units of degrees so they can simply be summed.
    orrientation += turn

    #since our direction constants are simply constants they cannot contain values for all 2*pi. So if our orrientation
    #goes 2*pi above or below some of our constants we reset them to said constant here.
        
    if orrientation < -90:
        orrientation += 360
    elif orrientation >180:
        orrientation += -360

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


#changes our x and y coordinates based on our orrientation
def move_bot(orrientation, x, y, turn, stepsize):
    #since the direction to move in and orrientation has already been selected and changed we simply move one gridsize
    #unit in that direction.
    if turn == c.BACKWARD:
        return x, y
    elif orrientation == c.NORTH:
        y += stepsize
    elif orrientation == c.EAST:
        x += stepsize
    elif orrientation == c.SOUTH:
        y += -stepsize
    elif orrientation == c.WEST:
        x += -stepsize

    return x, y

########################################################################################################################
def generate_movement_list(movelist, orrientation, stepsize=c.RADIUS):
    movelength = 0
    instructions = []

    for i in range(len(movelist)):
        if i == 0:
            currentx = movelist[i][0]
            currenty = movelist[i][1]

        else:
            prevx = currentx
            prevy = currenty

            currentx = movelist[i][0]
            currenty = movelist[i][1]

            neworrientation = m.degrees(m.atan2(currenty - prevy, currentx - prevx))

            if neworrientation < -90:
                neworrientation += 360
            elif neworrientation > 180:
                neworrientation += -360

            if orrientation == neworrientation:
                movelength += stepsize

            else:

                instructions.append(movelength)
                movelength = stepsize

                turn = neworrientation - orrientation

                if turn < -90:
                    turn += 360
                elif turn > 180:
                    turn += -360

                instructions.append(turn)
                orrientation = neworrientation

    instructions.append(movelength)
    
    turn = c.EAST - orrientation
    if turn < -90:
        turn += 360
    elif turn > 180:
        turn += -360
        
    instructions.append(turn)

    return instructions

