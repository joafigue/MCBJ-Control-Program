""" Module no_measure_plot - Continuous plotting of the conductance data

This program will perform continuous measurements of the conductance data
and will plot it. This program should be used for analysis of the data and
the experimental setup.
"""
__author__ = "Joaquin Figueroa"

import os
import sys
import modules.utilities as utl
import modules.configuration as conf
import modules.motor_break as mb
from modules.motor_break import stop # Important function to stop everything

def parse_options(argv):        #(ref:src-no-measure-parse-args)
    """ Check if the user provided a configuration file, otherwise use default """
    try:
        filename = argv[1]      # argv[0] is the scriptname
    except:
        directory = utl.get_script_root_path()
        filename = "Measurement_deafult_config.yaml"
        filename = os.path.join(directory, filename)
    return filename

def build_config_if_file_exists(filename): #(ref:src-no-measure-config)
    """ If the file exists build configuration, otherwise use hardcoded values"""
    if os.path.isfile(filename):
        return conf.yaml_build_config_from_file(filename)
    return conf.program_config()

def main(filename):             #(ref:src-no-measure-main)
    """ Continuous conductance measurement main program

    This is the main loop. It will just call the continuous measurement
    and will show the conductance measurement continuously
    """
    config = build_config_if_file_exists(filename) #
    iv_config = config.iv_config

    state = mb.no_motor_continuous_plot(iv_config)
    if state >= mb.MB_STATE.ERROR_STATUS:
        print("Detected an error during continuous measurement")
        print("Please Investigate")
    print("PROGRAM FINISHED")

if __name__ == "__main__":
    CONFIGFILE = parse_options(sys.argv)
    main(CONFIGFILE)
    stop()
