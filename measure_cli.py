""" Module measure_cli - Performs full break-juncture measurement

This File has the control loop necessary to perform the measuremnet using
the break-junction technique.

This program needs the path to a single configuration file to setup the run.
If the file is not provided, a default file will be used.

This program will (subject to the configuration file):
1- Operate the motor to break the juncture and find the operating point
2- Perform the measurment using the piezoelectric actuator.
"""
__author__ = "Joaquin Figueroa"

import os
import sys
import modules.adwin_driver as adw
import modules.utilities as utl
import modules.configuration as conf
import modules.piezo_measure as pm
import modules.motor_break as mb
from modules.motor_break import stop # Important function to stop everything

def parse_options(argv):
    """ Check if the user provided a configuration file, otherwise use default """
    try:
        filename = argv[1]      # argv[0] is the scriptname
    except:
        filename = default_config_file()
    return filename

def default_config_file():
    """ Function to determine the default configuration file to use

    This function is used to deterine the configuration file to be used.
    Note that in this function we can set a "new" default file by hand, which can
    be used to pass the configuration file without running the program through the
    Command line.
    """

    custom_config_file = "F:\joaquin_rewrite\data\New Folder\Configuration_file_20170131_114342.yaml"
    if os.path.isfile(custom_config_file):
        return custom_config_file
    directory = utl.get_script_root_path()
    filename = "Measurement_deafult_config.yaml"
    filename = os.path.join(directory, filename)
    return filename

def build_config_if_file_exists(filename):
    """ If the file exists build configuration, otherwise use hardcoded values"""
    if os.path.isfile(filename):
        return conf.yaml_build_config_from_file(filename)
    return conf.program_config()

def main(filename):
    """ Closed loop for measurement using the MCBJ technique

    The main loop, This function will perform the measurement and save the data.
    This Program will build the configuration from the provided file. Then:
    - If the user specified it it will move the motor to the operation point
    - If the system is in the operation point, will perform the measuerement
    - For each measurement (trace) will save and plot the Data
    """
    utl.closefigs()
    config = build_config_if_file_exists(filename) #
    dconfig = config.display_config
    hconfig = config.hist_config
    iv_config = config.iv_config
    failure_count = 0

    state = mb.MB_STATE.READY_ON_POINT
    if iv_config.get_move_motor(): #
        state = mb.motor_break_print_plot(iv_config)

    if state == mb.MB_STATE.READY_ON_POINT: #
        trace = 1
        traces = config.save_config.get_traces()
        adw_hist = adw.adwin_hist_driver(hconfig)
        hist_plotter = pm.histogram_plot_data_class(dconfig)

        while trace <= traces:
            break_hist, make_hist = adw_hist.measure_and_get_histogram(trace)
            hist_save = pm.histogram_save_data_class(break_hist, make_hist, config)
            hist_plotter.update_histogram_plt_data(hist_save)
            hist_plotter.plot_break_make_trace()
            hist_plotter.plot_histogram_1D()
            hist_plotter.plot_histogram_2D()
            if adw_hist.successful_measurement():
                hist_save.save_data(trace)
                trace += 1
            else:
                failure_count += 1
                if failure_count > 100:
                    break
        print("PROGRAM FINISHED Successfully")
        print("Program ended at {0} traces".format(trace-1))
        print("Found {0} traces with errors".format(failure_count))



if __name__ == "__main__":
    CONFIGFILE = parse_options(sys.argv)
    main(CONFIGFILE)
    stop()
