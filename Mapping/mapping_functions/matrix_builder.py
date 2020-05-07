'''
Function for creating matricies for map routing algorithms

Author: Kristian Melo
Version: 15 Jan 2018
'''
########################################################################################################################
##Imports
########################################################################################################################
from Mapping.constants import  constants as c
########################################################################################################################
#To use Dijkstras algorithm we need a list of "edges". this is a n x 3 matrix where each row contains the start point,
#end point, and distance.
def build_edges_matrix(lawn):

    edges = []

    #loop through all nodes in list
    for nodes in lawn:

        #loop through all the neighbors in a given node
        for i in nodes.neighbors:

            #add new edge between the given node and its neighbore to the list of edges
            #note the length is always gridsize since neighbores are always adjacent squares
            edges.append([str(nodes.location), str(i), c.GRIDSIZE])


    return edges


########################################################################################################################
'''
#legacy code, keeping in case of future changes
def build_distance_matrix(lawn):

    movelist = []
    obslist = []

    for node in lawn:
        if node.type != 9:
            movelist.append(node)
        else:
            obslist.append(node)

    distance = np.zeros((len(movelist), len(movelist)))

    i,j = 0,1
    while i < len(movelist):
        while j < len(movelist):
            x1 = movelist[i].location[0]
            x2 = movelist[j].location[0]
            y1 = movelist[i].location[1]
            y2 = movelist[j].location[1]
            r = m.hypot(x2-x1,y2-y1)
            if col.obstacleDetection(obslist, x1, y1, x2, y2) == False:
                distance[i, j] = r

            j += 1

        i += 1
        j = i + 1

    return distance
'''