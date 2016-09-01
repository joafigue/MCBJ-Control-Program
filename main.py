# [[file:Measure_samples.org::*Main%20Loop][Main\ Loop:1]]
#################################################################
## @file    Main.py
#  @author  Joaquin Figueroa
#  @brief   Main file for measuring break-junction experiments
#
#  @details This is the main file for the program used to
#           measure samples using the break-junction technique.
#           This program provides a GUI to control the execution
#           based on providing the tools to configure a run.
#           The program automates the whole procedure by:
#           1- Automating the creation of the break junction
#           using the motor
#           2- Automating the measurement process using a piezo
#           actuator.
#################################################################
# Main\ Loop:1 ends here

# [[file:Measure_samples.org::*Main%20Loop][Main\ Loop:2]]
import sys
from modules.ui_config import *
from modules.motor_break import *
from modules.piezo_measure import *
# Main\ Loop:2 ends here

# [[file:Measure_samples.org::*Main%20Loop][Main\ Loop:3]]
############################################################
## @fn    : main_exit
#  @brief : Terminates program execution
############################################################
def main_exit(config) :
    print("Program Finished successfully")
    sys.exit()
# Main\ Loop:3 ends here

# [[file:Measure_samples.org::*Main%20Loop][Main\ Loop:4]]
############################################################
## @fn      : main_motor_break
#  @details : Commands the motor to break the gold channel
#             creating a break-junction and then joins it
#             again leaving it ready for measurement
############################################################
def main_motor_break(config):
    motor_break_juncture()
# Main\ Loop:4 ends here

# [[file:Measure_samples.org::*Main%20Loop][Main\ Loop:5]]
############################################################
## @fn      : main_measure
#  @details : Measures the transport properties of the
#             sample by creating the break-junction with the
#             motor, and using the piezo to measure
############################################################
def main_measure(config):
    motor_break_juncture()
    measure_sample()
# Main\ Loop:5 ends here

# [[file:Measure_samples.org::*Main%20Loop][Main\ Loop:6]]
############################################################
## @fn      : execute_ui_cmd
#  @details : Analyzed the command chosen by the user and
#             executes it. Options are:
#             1- End program
#             2- only perform break-junction
#             3- perform full measurement of the sample
############################################################
def execute_ui_cmd(ui_cmd,config) :
    switch = {
        UI_CMD.EXIT    : main_exit,
        UI_CMD.M_BREAK : main_motor_break,
        UI_CMD.MEASURE : main_measure,
    }
    cmd = switch.get(ui_cmd, sys.exit)
    cmd(config)
# Main\ Loop:6 ends here

# [[file:Measure_samples.org::*Main%20Loop][Main\ Loop:7]]
############################################################
## @details : Main loop. Executes UI Cmd until the user end
##            the program
############################################################
def main():
    while True :
        ui_config = ui_get_gui_config()
        ui_cmd    = ui_config.cmd
        config    = ui_config.config
        config._b_params.print_all()
        execute_ui_cmd(ui_cmd,config)

if __name__ == "__main__":
    main()
# Main\ Loop:7 ends here
