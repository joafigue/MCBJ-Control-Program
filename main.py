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

import sys
import modules.ui_config as UI
import modules.motor_break as MB
import modules.piezo_measure as PM

############################################################
## @fn    : main_exit
#  @brief : Terminates program execution
############################################################
def main_exit() :
    print("Program Finished successfully")
    sys.exit()

############################################################
## @fn      : main_motor_break
#  @details : Commands the motor to break the gold channel
#             creating a break-junction and then joins it
#             again leaving it ready for measurement
############################################################
def main_motor_break():
    MB.motor_break_juncture()

############################################################
## @fn      : main_measure
#  @details : Measures the transport properties of the
#             sample by creating the break-junction with the
#             motor, and using the piezo to measure
############################################################
def main_measure():
    MB.motor_break_juncture()
    PM.measure_sample()

############################################################
## @fn      : execute_ui_cmd
#  @details : Analyzed the command chosen by the user and
#             executes it. Options are:
#             1- End program
#             2- only perform break-junction
#             3- perform full measurement of the sample
############################################################
def execute_ui_cmd(ui_cmd) :
    switch = {
        UI.CMD.EXIT    : main_exit,
        UI.CMD.M_BREAK : main_motor_break,
        UI.CMD.MEASURE : main_measure,
    }
    cmd = switch.get(ui_cmd, sys.exit)
    cmd()

############################################################
## @details : Main loop. Executes UI Cmd until the user end
##            the program
############################################################
while True :
    ui_cmd=UI.CMD.EXIT
    execute_ui_cmd(ui_cmd)
