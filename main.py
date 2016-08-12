import sys
import modules.ui_config as ui
import modules.motor_break as mb
import modules.piezo_measure as pm

############################################################
## @fn    : main_exit
#  @brief : Terminates program execution
############################################################
def main_exit() :
    print("exit")
    sys.exit()

############################################################
## @fn      : main_motor_break
#  @details : Commands the motor to break the gold channel
#             creating a break-junction and then joins it
#             again leaving it ready for measurement
############################################################
def main_motor_break():
    print("break")
    mb.motor_break_juncture()

############################################################
## @fn      : main_measure
#  @details : Measures the transport properties of the
#             sample by creating the break-junction with the
#             motor, and using the piezo to measure
############################################################
def main_measure():
    print("measure")
    mb.motor_break_juncture()
    pm.measure_sample()

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
        ui.cmd.exit    : main_exit,
        ui.cmd.m_break : main_motor_break,
        ui.cmd.measure : main_measure,
    }
    cmd = switch.get(ui_cmd, sys.exit)
    cmd()

############################################################
## @details : Main loop. Executes UI Cmd until the user end
##            the program
############################################################
while True :
    ui_cmd=ui.cmd.m_break
    execute_ui_cmd(ui_cmd)
