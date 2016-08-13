#################################################################
## @file    ui_config.py
#  @author  Joaquin Figueroa
#  @date    Fri Aug 12 2016
#  @brief   Provides a UI for configuring the experiment
#
#  @details This file provides a GUI for the user to be able to
#           configure the experiment and run it.
#################################################################
from PyQt4 import QtGui

############################################################
## @class   UI_RESULT
#  @details This class has the return type of the UI class
#           The return type has:
#           1- Command to be executed (exit, measure)
#           2- Configuration for the measurements
############################################################
class UI_RESULT:
    def __init__(self, cmd, config):
        self.cmd    = cmd
        self.config = config

############################################################
## @class  CMD
#  @brief  UI calss to encode the possible commands for the
#         program
############################################################
class CMD:
    EXIT    = 0
    M_BREAK = 1
    MEASURE = 2

############################################################
## @class   UI_CONFIG
#  @details This class stores all configuration values to be
#           used for the measurements.
############################################################
class UI_CONFIG:
    def __init__(self):
        self._basic_param = basic_params()
        self._adv_param = adv_param()
        self._presentation = presentation()






