# LawnBot
This project is the full software for an autonomous law-mowing robot. 

## Main Processing Unit
A main system-on-a-chip unit contains the high-level software for controlling and interfacing all modules of the robot. This process manages all system processes and communication with other systems. 

## Computer Vision
OpenCV is used to rapidly process images and identify obstacles, and thereafter report their location relative to the robot.

## Sonar Sensing
An array of sonar sensors are used to assist with obstacle identification.

## Power Management
A coulomb-counter circuit measures the battery discharge. A dedicated microcontroller reads the measurements and reports reamining battery live to main control system.

## Mobile Application
A mobile (android) application is used to start and monitor the robot. Bluetooth communication (pybluez) is used update the application in real-time with the robot status, location, and remaining battery. 

## Mapping 
Intelligent mapping keeps track of where the robot has been and location of identified obstacles. By default the robot will attempt to traverse a zig-zag pattern route. Re-runs of know lawns with obstacales will have an optimized route.  

## Robot Movement
Stepper-motors are used to execute movement commands. An absolute orientation sensor is used to measure and monitor the oreintation of the robot during a turn movement.
