'''
This function plots a graphical representation of the lawn used for testing simulations

Author: Kristian Melo
Version: 18 Jan 2018
'''
########################################################################################################################
##Imports
########################################################################################################################
import matplotlib.pyplot as plt
import math as m
import pylab
from Mapping import constants as c
########################################################################################################################

def plot_lawn(lawn, movelist):

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')
    size = 120

    #plot all nodes in the list, color indicating type
    for node in lawn:

        if node.type == 2:
            b = ax1.scatter(node.location[0], node.location[1], c='blue', s=size)
        elif node.type == 3:
            g = ax1.scatter(node.location[0], node.location[1], c='limegreen', s=size)
        elif node.type == 9:
            r = ax1.scatter(node.location[0], node.location[1], c='red', s=size)

    p = ax1.scatter(0, 0, c='cyan', s=size)

    oldx = 0
    oldy = 0
    arrowlength = 0.3
    count = 0
    #plot arrows showing direction of movement
    plt.ion()
    for point in movelist:
        if count == 0:
            count = 1
        else:
            if oldx != point[0] or oldy != point[1]:
                anglerad = m.atan2(point[1] - oldy, point[0] - oldx)
                xoffset = m.cos(anglerad)*arrowlength*2
                yoffset = m.sin(anglerad)*arrowlength*2
                ax1.arrow(oldx, oldy, point[0]-oldx - xoffset, point[1]-oldy - yoffset,
                          head_width=0.3,
                          head_length=arrowlength,
                          fc='k',
                          ec='k')

            oldx = point[0]
            oldy = point[1]
            plt.pause(0.00005)

    y = ax1.scatter(oldx, oldy, c='yellow', s=size)

    plt.title('First pass obstacle finding', fontsize=20)
    plt.xlabel('X Position', fontsize=15)
    plt.ylabel('Y Position', fontsize=15)
    plt.legend((g,r,p,y),
               ('Visited', 'Obstacle','Start location', 'End location'),
               scatterpoints=1,
               bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.ioff()
    plt.show()


def plot_node_layout(tspnodes):
    '''
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')

    for node in tspnodes:

        ax1 = plt.scatter(node.locx, node.locy, edgecolors='r', s=1600, facecolors='none')


    plt.show()
    '''
    axes = pylab.axes()

    for node in tspnodes:
        if node.type == 2:
            circle = pylab.Circle((node.location[0], node.location[1]), radius=c.RADIUS/2, edgecolor='cyan',facecolor='none')
            axes.add_patch(circle)

        else:
            circle = pylab.Circle((node.location[0], node.location[1]), radius=c.RADIUS / 2, edgecolor='r',
                                  facecolor='none')
            axes.add_patch(circle)

    pylab.axis('scaled')
    pylab.show()

    return
