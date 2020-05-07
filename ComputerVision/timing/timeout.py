'''
A signal handler to raise an exception if a given time has elapsed, in this case to be used with a function to see how
long it has been running. Some code chunks borrowed from:
https://stackoverflow.com/questions/2281850/timeout-function-if-it-takes-too-long-to-finish

Author: Hayden Banting
Version: 02 December 2017
'''
########################################################################################################################
## Imports
########################################################################################################################
import errno
import os
import signal
import warnings
from functools import wraps
########################################################################################################################
class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):

    def decorator(func):

        def _handle_timeout(signum, frame):
            #raise TimeoutError(error_message)
            warnings.warn(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(signal.ITIMER_REAL, seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator
########################################################################################################################