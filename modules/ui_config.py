# [[file:../Measure_samples.org::*User%20Interface][User\ Interface:1]]
#################################################################
## @file    ui_config.py
#  @author  Joaquin Figueroa
#  @date    Fri Aug 12 2016
#  @brief   Provides the definitions and parameters for the UI
#
#  @details This file provides a all the necessary helper
#           functions to interface the different parameters
#           with the program.
#################################################################
from PyQt4 import QtGui
from PyQt4 import QtCore
import sys
JUNCTURE_VOLTAGE_DFLT = 0.1  #[V]
PIEZO_SPEED_BREAKING_DFLT = 0       #[V/S]
DATA_DIRECTORY_DFLT = "./Data"
NUMBER_TRACES_DFLT = 5000  # Measurement Cycles
piezo_start_V = 0.0         # V
high_G = 30.0              # G0
inter_G = 20.0              # G0
low_G = 10.0              # G0
piezo_speed_breaking1 = 300.0        # V/s
piezo_speed_breaking2 = 300.0        # V/s (30 to 300) Este es el que se puede cambiar
piezo_speed_making = 500.0        # V/s
#post_breaking_voltage = 230.0       #
post_breaking_voltage = 300.0       # cambia cuanto abro despues de que rompo
nGbins = 251
nDbins = 161
xmin = -0.5 # nm
xmax = 2    # nm
Gmin = 1e-7 # G0
Gmax = 10   # G0
todoJUNCTURE_VOLTAGE_DFLT = 0  #[V]
todoPIEZO_SPEED_DFLT = 0       #[V/S]
todoDATA_DIRECTORY_DFTL = "./Data"
# User\ Interface:1 ends here

# [[file:../Measure_samples.org::*UI%20-%20Program%20Interface][UI\ -\ Program\ Interface:1]]
############################################################
## @class   UI_CONFIG
#  @details This class has the return type of the UI class
#           The return type has:
#           1- Command to be executed (exit, measure)
#           2- Configuration for the measurements
############################################################
class UI_CONFIG:
    def __init__(self):
        self.cmd    = UI_CMD.EXIT
        self.config = UI_CONFIG_PARAMS()

    ############################################################
    ## @brief   Updates the ui_cmd with a new one
    ############################################################
    def update_cmd(self, new_cmd):
        self.cmd = new_cmd

    ############################################################
    ## @brief   Updates the config with a new one
    ############################################################
    def update_config(self, new_config):
        self.config = new_config
# UI\ -\ Program\ Interface:1 ends here

# [[file:../Measure_samples.org::*UI%20command][UI\ command:1]]
############################################################
## @class  CMD
#  @brief  UI calss to encode the possible commands for the
#         program
############################################################
class UI_CMD:
    EXIT    = 0
    M_BREAK = 1
    MEASURE = 2
# UI\ command:1 ends here

# [[file:../Measure_samples.org::*UI%20Configuration][UI\ Configuration:1]]
############################################################
## @class   UI_CONFIG
#  @details This class stores all configuration values to be
#           used for the measurements.
############################################################
class UI_CONFIG_PARAMS:
    def __init__(self):
        self._basic_params = basic_params()
        self._adv_params = adv_params()
        self._presentation = presentation()
# UI\ Configuration:1 ends here

# [[file:../Measure_samples.org::*UI%20Configuration][UI\ Configuration:2]]
def ui_get_gui_config():
    retval = run_gui()
    return retval
# UI\ Configuration:2 ends here

# [[file:../Measure_samples.org::ui-basic-params-defaults][ui-basic-params-defaults]]
JUNCTURE_VOLTAGE_DFLT = 0.1  #[V]
PIEZO_SPEED_BREAKING_DFLT = 0       #[V/S]
DATA_DIRECTORY_DFLT = "./Data"
NUMBER_TRACES_DFLT = 5000  # Measurement Cycles
# ui-basic-params-defaults ends here

# [[file:../Measure_samples.org::*UI%20-%20Basic%20parameters][UI\ -\ Basic\ parameters:2]]
class basic_params:
      def __init__(self):
            self.restore_defaults()
      def restore_defaults(self):
            self.juncture_voltage = JUNCTURE_VOLTAGE_DFLT
            self.piezo_speed_breaking = PIEZO_SPEED_BREAKING_DFLT
            self.data_directory = DATA_DIRECTORY_DFLT
            self.number_traces = NUMBER_TRACES_DFLT
# UI\ -\ Basic\ parameters:2 ends here

# [[file:../Measure_samples.org::ui-config-bp-interface][ui-config-bp-interface]]

# ui-config-bp-interface ends here

# [[file:../Measure_samples.org::*UI%20-%20Advanced%20parameters][UI\ -\ Advanced\ parameters:1]]
class adv_params:
      def __init__(self):
            self.asdf = 1
# UI\ -\ Advanced\ parameters:1 ends here

# [[file:../Measure_samples.org::ui-config-ap-interface][ui-config-ap-interface]]

# ui-config-ap-interface ends here

# [[file:../Measure_samples.org::ui-advanced-params-defaults][ui-advanced-params-defaults]]
piezo_start_V = 0.0         # V
high_G = 30.0              # G0
inter_G = 20.0              # G0
low_G = 10.0              # G0
piezo_speed_breaking1 = 300.0        # V/s
piezo_speed_breaking2 = 300.0        # V/s (30 to 300) Este es el que se puede cambiar
piezo_speed_making = 500.0        # V/s
#post_breaking_voltage = 230.0       #
post_breaking_voltage = 300.0       # cambia cuanto abro despues de que rompo
nGbins = 251
nDbins = 161
xmin = -0.5 # nm
xmax = 2    # nm
Gmin = 1e-7 # G0
Gmax = 10   # G0
# ui-advanced-params-defaults ends here

# [[file:../Measure_samples.org::ui-presentation-params-defaults][ui-presentation-params-defaults]]
todoJUNCTURE_VOLTAGE_DFLT = 0  #[V]
todoPIEZO_SPEED_DFLT = 0       #[V/S]
todoDATA_DIRECTORY_DFTL = "./Data"
# ui-presentation-params-defaults ends here

# [[file:../Measure_samples.org::*UI%20-%20Presentation][UI\ -\ Presentation:2]]
class presentation:
      def __init__(self):
            self.asdf = 1
# UI\ -\ Presentation:2 ends here

# [[file:../Measure_samples.org::ui-config-pp-interface][ui-config-pp-interface]]

# ui-config-pp-interface ends here

# [[file:../Measure_samples.org::*UI%20-%20GUI][UI\ -\ GUI:1]]
############################################################
## @brief   Runs the GUI for the program
############################################################
def run_gui():
    app = QtGui.QApplication(sys.argv) # Create "aplication"
    config_window = ui_config_window() # Instantiate widget
    app.exec_()                        # Execute appliaction
    return config_window.ui_config
# UI\ -\ GUI:1 ends here

# [[file:../Measure_samples.org::*Configuration%20Window][Configuration\ Window:1]]
############################################################
## @class   ui_config_window
#  @brief   Provides The UI window for the program
#
#  @details This Object provides the user interface to
#           configure the measurements and which procedures
#           to take.
#           The object has the description of the window
#           composed by the text dialogs and the buttons
#           to run the simulation, which are stored as
#           part of the window. The object also provides
#           the functions to interface it.
#           - initUI: Initialize the window
############################################################
class ui_config_window(QtGui.QWidget):
    # Default constructor
    def __init__(self):
        super(ui_config_window, self).__init__()
        self.initUI()

    ############################################################
    ## @brief   Initializes the window
    #  @details Initialized the window components, which are the
    #           configs, the buttons and the configuration.
    #           Also ensures the layout of the UI elements
    ############################################################
    def initUI(self):    #
        self.ui_config = UI_CONFIG() #

        buttons_layout = ui_create_buttons_layout(self) #
        config_layout  = ui_create_config_layout(self)  #
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(config_layout)
        vbox.addLayout(buttons_layout)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')
        self.show()

    ############################################################
    ## @brief   Interface to close the window and excecute a
    #           command
    ############################################################
    def close_with_cmd(self, cmd): #
        self.ui_config.update_cmd(cmd)
        QtCore.QCoreApplication.instance().quit()
# Configuration\ Window:1 ends here

# [[file:../Measure_samples.org::*Buttons%20Layout][Buttons\ Layout:1]]
############################################################
## @brief   Creates buttons layout and returns it
#
#  @details The function creates a layout to place the
#           buttons to perform the different actions of the
#           program.
#           The layout creates the following buttons:
#           - Quit Button: Ends the program
#           - Break Button: Use the motor do break junction
#           - Measure Button: Do a break junction and then
#                             use the piezo to measure
############################################################
def ui_create_buttons_layout(widget):
    # Quit Button
    quit_button = QtGui.QPushButton("Quit")
    quit_button.clicked.connect(
        lambda: widget.close_with_cmd(UI_CMD.EXIT)) 
    quit_button.setToolTip("Terminates the program")
    # Break Button
    break_button = QtGui.QPushButton("Only break")
    break_button.clicked.connect(
        lambda: widget.close_with_cmd(UI_CMD.M_BREAK))
    break_button.setToolTip("Use the motor to create a break junction.")
    # Measure Button
    measure_button = QtGui.QPushButton("Full Measure")
    measure_button.clicked.connect(
        lambda: widget.close_with_cmd(UI_CMD.MEASURE))
    measure_button.setToolTip(
        "Performs measurement using the motor and piezo")

    # Build Layout
    hbox = QtGui.QHBoxLayout()
    hbox.addStretch(1)
    hbox.addWidget(quit_button)
    hbox.addWidget(break_button)
    hbox.addWidget(measure_button)

    vbox = QtGui.QVBoxLayout()
    vbox.addStretch(1)
    vbox.addLayout(hbox)
    return vbox
# Buttons\ Layout:1 ends here

# [[file:../Measure_samples.org::config-param-layout][config-param-layout]]
############################################################
## @brief   Describes the configuration parameters layout
#
#  @details This function provides the layout for the portion
#           of the window that allows the user to configure
#           the parameters for the run.
#           The layout is split in 3 vertical sections one
#           with each parameter group.
#           Each group is preceded by a small label
#           identifying the group
############################################################
def ui_create_config_layout(ui_config_window):
    # Define each group layout
    basic_param_layout = ui_basic_param_layout(ui_config_window)
    adv_param_layout = ui_adv_param_layout(ui_config_window)
    presentation_param_layout = ui_presentation_param_layout(ui_config_window)
    # Define the labels
    basic_label = QtGui.QLabel("---- Basic Parameters ----")
    adv_label = QtGui.QLabel("---- Advanced Parameters ----")
    presentation_label = QtGui.QLabel("---- Presentation Parameters ----")
    # Configure the layout
    vbox = QtGui.QVBoxLayout()
    vbox.addStretch(1)
    vbox.addWidget(basic_label)
    vbox.addLayout(basic_param_layout)
    vbox.addWidget(adv_label)
    vbox.addLayout(adv_param_layout)
    vbox.addWidget(presentation_label)
    vbox.addLayout(presentation_param_layout)
    return vbox
# config-param-layout ends here

# [[file:../Measure_samples.org::*Configuration%20Parameters%20Layout][Configuration\ Parameters\ Layout:2]]
def ui_basic_param_layout(ui_config):
    jv_label = QtGui.QLabel("Juncture Voltage")
    psb_label = QtGui.QLabel("Piezo Speed")
    data_dir_label = QtGui.QLabel(str(ui_config.ui_config.config._basic_params.data_directory))
    traces_label = QtGui.QLabel("Number Traces")

    jv_ed = QtGui.QLineEdit()
    psb_ed = QtGui.QLineEdit()
    traces_ed = QtGui.QLineEdit()
    dir_btn = QtGui.QPushButton('Change Directory')

    jv_ed.setText(str(ui_config.ui_config.config._basic_params.juncture_voltage))
    psb_ed.setText(str(ui_config.ui_config.config._basic_params.piezo_speed_breaking))
    traces_ed.setText(str(ui_config.ui_config.config._basic_params.number_traces))

    dir_btn.clicked.connect(lambda: showDialog(ui_config))

    grid = QtGui.QGridLayout()
    grid.setSpacing(10)

    grid.addWidget(jv_label,1,0)
    grid.addWidget(jv_ed,1,1)

    grid.addWidget(psb_label,2,0)
    grid.addWidget(psb_ed,2,1)

    grid.addWidget(traces_label,3,0)
    grid.addWidget(traces_ed,3,1)

    grid.addWidget(data_dir_label,4,0)
    grid.addWidget(dir_btn,4,1)

    return grid

def showDialog(ui_config):
    fname = QtGui.QFileDialog.getExistingDirectory(ui_config, 'Open file',
            '/home')
    print(fname)

def ui_adv_param_layout(ui_config):
    return ui_basic_param_layout(ui_config)

def ui_presentation_param_layout(ui_config):
    return ui_basic_param_layout(ui_config)
# Configuration\ Parameters\ Layout:2 ends here
