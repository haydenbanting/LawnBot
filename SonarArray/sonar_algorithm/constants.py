'''
A file for all the constants relevant to the sonar sensors.

Author: Hayden Banting
Version: 22 December 2017
'''
########################################################################################################################
c0 = 343            # Speed of sound [m/s]
eps_sonar = 0.003   # Device position error
dmax = 5            # Maximum range of sonars
alpha = 15          # Beam angle (degrees)
########################################################################################################################
sonar_positions = [(0, 0.14), (0.20, 0.11), (0.19, 0), (0.20, -0.11), (0.0, -0.14)]   # With respect to bot (mounting positions)
sonar_angles = [90, -10, 0, 10, -90]                    # With respect to bot (mounting angles)
########################################################################################################################
DEG_TO_RAD = 0.0174533
########################################################################################################################