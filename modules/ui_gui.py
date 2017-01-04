#################################################################
## @file    ui_gui.py
#  @author  Joaquin Figueroa
#  @date    Fri Aug 12 2016
#  @brief   Provides the GUI for configuring the experiment
#
#  @details This file provides a GUI for the user to be able to
#           configure the experiment and run it.
#################################################################
from PyQt4 import QtGui
from PyQt4 import QtCore
import modules.ui_config
import sys

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

############################################################
## @brief   Runs the GUI for the program
############################################################
def run_gui():
    app = QtGui.QApplication(sys.argv) # Create "aplication"
    config_window = ui_config_window() # Instantiate widget
    app.exec_()                        # Execute appliaction
    return config_window.ui_config

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
        self.ui_config = modules.ui_config.UI_CONFIG() #

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
        lambda: widget.close_with_cmd(modules.ui_config.UI_CMD.EXIT)) 
    quit_button.setToolTip("Terminates the program")
    # Break Button
    break_button = QtGui.QPushButton("Only break")
    break_button.clicked.connect(
        lambda: widget.close_with_cmd(modules.ui_config.UI_CMD.M_BREAK))
    break_button.setToolTip("Use the motor to create a break junction.")
    # Measure Button
    measure_button = QtGui.QPushButton("Full Measure")
    measure_button.clicked.connect(
        lambda: widget.close_with_cmd(modules.ui_config.UI_CMD.MEASURE))
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

def ui_basic_param_layout(window):
    basic_params = window.ui_config.config._b_params ## Fix this
    # Num parameters fields
    jv_label, jv_text = num_param_label_textbox(basic_params.juncture)
    ps_label, ps_text = num_param_label_textbox(basic_params.piezo_speed)
    tr_label, tr_text = num_param_label_textbox(basic_params.traces)
    # Change directory dialog and fields
    dir_label = QtGui.QLabel(basic_params.data_dir.path)
    dir_btn = QtGui.QPushButton('Change Directory')
    dir_btn.clicked.connect(lambda: showDialog(window,dir_label))
    # Add fields to the layout
    grid = QtGui.QGridLayout()
    grid.setSpacing(10)

    grid.addWidget(jv_label,1,0)
    grid.addWidget(jv_text,1,1)

    grid.addWidget(ps_label,2,0)
    grid.addWidget(ps_text,2,1)

    grid.addWidget(tr_label,3,0)
    grid.addWidget(tr_text,3,1)

    grid.addWidget(dir_label,4,0)
    grid.addWidget(dir_btn,4,1)

    return grid

def ui_adv_param_layout(window):
    return ui_basic_param_layout(window)

def ui_presentation_param_layout(window):
    return ui_basic_param_layout(window)

#############################################################
## @class   QValidator_num_param
#  @brief   Validator for numerical parameters
#
#  @details This class provides a specialization of the
#           QValidator class for numerical parameters and
#           allow only values that are valid for the
#           parameter.
#############################################################
class QValidator_num_param(QtGui.QValidator):
        #############################################################
        ## @brief   Initialization function, with the parameter
        #############################################################
        def __init__(self, param): #
            QtGui.QValidator.__init__(self)
            self.param = param
        #############################################################
        ## @brief   Validate function using the parameter validation
        #           Ensures data is a number.
        #############################################################
        def validate(self, text, pos):#
                try:
                        num = float(text)
                except ValueError:
                        return (QtGui.QValidator.Invalid, text, pos)

                if self.param.validate(num):
                        self.param.update(num)
                        return (QtGui.QValidator.Acceptable, text,pos)
                return (QtGui.QValidator.Invalid, text, pos)
# src-qvalidator-num-param ends here

#############################################################
## @brief   Creates a label and textbox for a numerical
#           parameter.
#############################################################
def num_param_label_textbox(parameter):
    label = QtGui.QLabel(parameter.name)
    textbox = QtGui.QLineEdit()
    param_validator = QValidator_num_param(parameter)
    textbox.setValidator(param_validator)
    textbox.setText(str(parameter.value))
    return (label, textbox)

def showDialog(window,dir_label):
    data_dir = window.ui_config.config._b_params.data_dir
    fname = QtGui.QFileDialog.getExistingDirectory(window, 'Open file',
            data_dir.path)
    if(fname):
        data_dir.update(fname)
        dir_label.setText(data_dir.path)
        print(data_dir.path)
