""" Module graphical_measure - Runs a GUI to configure and the measures.

This program runs a Graphical User Interface to generate a configuration file.
Using the configuration file this program will either:
1- Avoid measurements to allow the user to diagnose the experimental setup
2- Perform the full measurement using the corresponding program.
"""

__author__ = "Joaquin Figueroa"

import sys
from modules.ui_gui import run_gui, UI_CMD
import measure_cli
import no_measure_plot
from modules.motor_break import stop

############################################################
## @fn    : main_exit
#  @brief : Terminates program execution
############################################################
def main_exit(config):
    print("Program Finished successfully")
    return False

############################################################
## @fn      : main_motor_break
#  @details : Commands the motor to break the gold channel
#             creating a break-junction and then joins it
#             again leaving it ready for measurement
############################################################
def main_no_op_measure(config_file):
    no_measure_plot.main(config_file)
    return True

############################################################
## @fn      : main_measure
#  @details : Measures the transport properties of the
#             sample by creating the break-junction with the
#             motor, and using the piezo to measure
############################################################
def main_measure(config_file):
    measure_cli.main(config_file)
    return True

############################################################
## @fn      : execute_ui_cmd
#  @details : Analyzed the command chosen by the user and
#             executes it. Options are:
#             1- End program
#             2- only perform break-junction
#             3- perform full measurement of the sample
############################################################
def execute_ui_cmd(ui_cmd, config_file):
    switch = {
        UI_CMD.EXIT    : main_exit,
        UI_CMD.NO_OP_PLOT : main_no_op_measure,
        UI_CMD.MEASURE : main_measure,
    }
    cmd = switch.get(ui_cmd, sys.exit)
    return cmd(config_file)

############################################################
## @details : Main loop. Executes UI Cmd until the user end
##            the program
############################################################
def main():
    run = True
    while run:
        ui_config, config = run_gui()
        ui_cmd    = ui_config.cmd
        print(config.get_config())
        config_filename = config.dump_config_file()
        run = execute_ui_cmd(ui_cmd, config_filename)

if __name__ == "__main__":
    main()
    stop()
