'''
Utility functions for reading and writing lawn (map) matrices from/to file.

Authors: Hayden Banting
Version: 10 January 2018
'''
########################################################################################################################
## Imports
import numpy as np
import time
import os
########################################################################################################################
## Default Values - move to constants file eventually
default_directory = 'Mapping/map_utilities/maps'
default_filename = 'lawn'
########################################################################################################################
def write_map_to_binary(array, directory=default_directory, filename=default_filename):
    '''
    Use this function to write any np.array to a binary file. The binary file is used instead of a .txt as the array
    may be multiple dimensions or contain non-basic data types or structures. By Default the lawn name is time-stamped.

    :param directory: directory where the map will be saved (string)
    :param filename: filename to give binary file (string)
    :param array: array to be saved (np.array)
    :return: None
    '''
    np.save(os.path.join(directory, filename + '_{}'.format(time.time())), array)

def read_map_from_binary(directory=default_directory, filename=default_filename):
    '''
    Use this function to load in a numpy array from a saved binary file.

    :param directory: directory where file is you want to load (string)
    :param filename: filename of file to load (string)
    :return: desired array (np.array)
    '''
    return np.load(os.path.join(directory, filename))

def check_for_binary_map(directory=default_directory):
    '''
    Use this function to fetch the names of all map files in a directory.

    :param directory: directory to check where map files may exist
    :return: filenames: list of filenames in directory (list)
    '''
    filenames = []
    for file in os.listdir(directory):
        filenames += [file]
    return filenames

def get_most_recent_map(directory=default_directory):
    '''
    Use this function as a high level function to read all the maps from some directory, sort them, and load in the
    most recent map array to be used.

    :param directory: directory to get most recent map from (string)
    :return: array of most recent map file (np.array)
    '''
    maps = check_for_binary_map(directory)
    most_recent = np.sort(maps)[::-1][0]
    return read_map_from_binary(directory, most_recent)
########################################################################################################################

