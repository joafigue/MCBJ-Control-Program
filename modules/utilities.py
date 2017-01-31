""" Module utilies - General purpose utilities

           This file stores several general purpose utilities
           that do not fit cleanly anywhere else. Obviously
           grat care has been tanke to ensure that this file
           is kept small
"""
__author__ = "Joaquin Figueroa"

import os
import inspect
import matplotlib.pyplot as plt

#############################################################
## @brief   Returns the path to the main.py directory
#  @details Uses the inspect functionality to determine
#           the current filename, then determines the
#           absolute path. Since this file is at a fixed
#           path from the script_root, it's returned
#############################################################
def get_script_root_path():
    fname = inspect.getframeinfo(inspect.currentframe()).filename
    module_path = os.path.dirname(os.path.abspath(fname))
    script_root_path = os.path.dirname(module_path)
    return script_root_path

def closefigs():
    for i in range(1000):
        plt.close(i)
