'''
Function for creating matricies for map routing algorithms

Author: Kristian Melo
Version: 15 Jan 2018
'''
########################################################################################################################
##Imports
########################################################################################################################
from Mapping.constants import constants as c
import math as m
import numpy as np
########################################################################################################################
def hardware_obsctale_check(x, y, orrientation, obs_nodes, obstacles, sonar):
    
    print('bot Location: ({},{})'.format(x,y))
    print('bot angle: {}'.format(orrientation))

    left_obs, straight_obs, right_obs = 0,0,0
    
    rot = np.array([(np.cos(orrientation), -1*np.sin(orrientation)),
                    (np.sin(orrientation), np.cos(orrientation))])

    for nodes in obs_nodes:
        
        print('Considering the sonar point ({},{})'.format(nodes[0], nodes[1]))
        #given nodes coordinates wrt our current location
        node_x = nodes[0] - x
        node_y = nodes[1] - y

        if orrientation == c.EAST: 
            node_x = node_x
            node_y = node_y

        elif orrientation == c.NORTH: 
            tempx = node_x
            tempy = node_y
            node_x = tempy
            node_y = -1 * tempx

        elif orrientation == c.WEST: 
            node_x = -1 * node_x
            node_y = -1 * node_y

        elif orrientation == c.SOUTH:                          
            tempx = node_x
            tempy = node_y
            node_x = -1 * tempy
            node_y = tempx

        if (node_y > 0.5 * c.GRIDSIZE) and (node_y < 1.5 * c.GRIDSIZE) and (node_x > -0.5 * c.GRIDSIZE) and (node_x < 0.5 * c.GRIDSIZE):
            left_obs += 1
        elif (node_y > -0.5 * c.GRIDSIZE) and (node_y < 0.5 * c.GRIDSIZE) and (node_x > 0.5 * c.GRIDSIZE) and (node_x < 1.5 * c.GRIDSIZE):
            straight_obs += 1
        elif (node_y < -0.5 * c.GRIDSIZE) and (node_y > -1.5 * c.GRIDSIZE) and (node_x > -0.5 * c.GRIDSIZE) and (node_x < 0.5 * c.GRIDSIZE):
            right_obs += 1

    if sonar:
        if left_obs > 0:
            obstacles[0] = 9
        if straight_obs > 0:
            obstacles[1] = 9
        if right_obs > 0:
            obstacles[2] = 9

    else:
        threshold = len(obs_nodes) * c.OBSTACLE_POINTS_THRESHOLD
        if left_obs > threshold:
            obstacles[0] = 9
        if straight_obs > threshold:
            obstacles[1] = 9
        if right_obs > threshold:
            obstacles[2] = 9


    return obstacles

def obstacleDetection(obslist, x, y, goalx, goaly):
    pathclear = False
    rangexmax = max(x, goalx)
    rangexmin = min(x, goalx)
    rangeymax = max(y, goaly)
    rangeymin = min(y, goaly)
    for node in obslist:
        if node.location[0] >= rangexmin and node.location[0] <= rangexmax and \
                        node.location[1] >= rangeymin and node.location[1] <= rangeymax:
            maxx = node.location[0] + c.gridsize * 0.5
            minx = node.location[0] - c.gridsize * 0.5
            maxy = node.location[1] + c.gridsize * 0.5
            miny = node.location[1] - c.gridsize * 0.5
            pathclear = lineSquareIntersect(x, y, goalx, goaly, minx, maxx, maxy, miny)
            if pathclear == True:
                return pathclear

    return pathclear
    #if pathclear == True:



def pointCircleIntersect(cx, cy, px, py):
    dx = abs(px-cx)
    dy = abs(py-cy)
    r = m.sqrt(2 * (0.5*c.gridsize)^2)

    if dx > r:
        return False
    if dy > r:
        return False

    return True

#liang-Barsky algorithm
#Returns true for intersection
def lineSquareIntersect(x1, y1, x2, y2, left, right, top, bottom):
    dx = x2 - x1 * 1.0
    dy = y2 - y1 * 1.0
    t0 = 0.0
    t1 = 1.0

    checks = ((-dx, -(left - x1)),
              (dx, right - x1),
              (-dy, -(bottom - y1)),
              (dy, top - y1))

    for p, q in checks:
        if p == 0 and q < 0:
            return False

        if p != 0:
            r = q / (p * 1.0)

            if p < 0:
                if r > t1:
                    return False
                elif r > t0:
                    t0 = r
            else:
                if r < t0:
                    return False
                elif r < t1:
                    t1 = r
    return True
