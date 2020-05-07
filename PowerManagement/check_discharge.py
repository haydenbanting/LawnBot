'''
Function which will return ture of false if the battery depth of discharge
is below an allowed amount. If true, the robot should return home.

'''
##############################################################################
TOTAL_COUNT = 38 * 3600
DEPTH_OF_DISCHAGE_THRESH = 0.5

def check_low_battery(count):
    
    if TOTAL_COUNT - count < TOTAL_COUNT * DEPTH_OF_DISCHAGE_THRESH: return 1
    return 0
    
    
    

    
    