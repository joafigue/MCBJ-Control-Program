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
import os
import inspect

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

# [[file:../Measure_samples.org::*UI%20Configuration%20Parameters][UI\ Configuration\ Parameters:1]]
############################################################
## @class   UI_CONFIG
#  @details This class stores all configuration values to be
#           used for the measurements.
############################################################
class UI_CONFIG_PARAMS:
    def __init__(self):
        self._b_params = basic_params()
        self._a_params = adv_params()
        self._p_params = presentation()
# UI\ Configuration\ Parameters:1 ends here

# [[file:../Measure_samples.org::*UI%20Configuration%20Parameters][UI\ Configuration\ Parameters:2]]
def ui_get_gui_config():
    retval = run_gui()
    return retval
# UI\ Configuration\ Parameters:2 ends here

# [[file:../Measure_samples.org::src-config-num-param-class][src-config-num-param-class]]
#############################################################
## @class   Numerical Parameter
#  @brief   All functionality related to the numerical
#           parameters
#
#  @details This class defines the basic behavior common to
#           all numerical parameters, including common
#           interfaces and values.
#############################################################
class numerical_parameter(object):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self,name,dflt_val,min_val,max_val):#
        self._dflt = dflt_val
        self._min = min_val
        self._max = max_val
        self.name = name
        self.reset()
    #############################################################
    ## @brief   restores the default value of the parameter
    #############################################################
    def reset(self): #
        self.value = self._dflt
    #############################################################
    ## @brief   Determines if a new value is in the permited
    #           range
    #############################################################
    def validate(self, val):#
        return (self._min <= val) & (val <= self._max)
    #############################################################
    ## @brief   Updates the stored value only if the new
    #           value is within range
    #############################################################
    def update(self,new_val):#
        if self.validate(new_val):
            self.value = new_val
    #############################################################
    ## @brief   Prints the parameter name and its value
    #############################################################
    def print_param(self):#
        print("%s = %f" % (self.name, self.value))
# src-config-num-param-class ends here

# [[file:../Measure_samples.org::src-config-int-param-class][src-config-int-param-class]]
#############################################################
## @class   Integer Parameter
#  @brief   All functionality related to the numerical
#           parameters that are to be treated as int
#############################################################
class integer_parameter(numerical_parameter):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self,name,dflt_val,min_val,max_val):
        _dflt = int(dflt_val)
        _min = int(min_val)
        _max = int(max_val)
        super(integer_parameter,self).__init__(name,_dflt,_min,_max)
    #############################################################
    ## @brief   Determines if a new int value is in the permited
    #           range, and integer
    #############################################################
    def validate(self, val): # 
        is_valid = super(integer_parameter,self).validate(val)
        return  float(val).is_integer() & is_valid
    #############################################################
    ## @brief   Prints the parameter name and its value
    #############################################################
    def print_param(self): # 
        print("%s = %d" % (self.name, self.value))
# src-config-int-param-class ends here

# [[file:../Measure_samples.org::*UI%20-%20Basic%20parameters][UI\ -\ Basic\ parameters:1]]
class basic_params:
      def __init__(self):
            self.juncture = juncture_voltage()
            self.piezo_speed = piezo_speed()
            self.traces = traces()
            self.paths = paths()
      def restore_defaults(self):
            self.juncture.reset()
            self.piezo_speed.reset()
            self.traces.reset()
            self.data_dir.reset()
      def print_all(self):
            print("--- Basic Parameters ---")
            self.juncture.print_param()
            self.piezo_speed.print_param()
            self.traces.print_param()
            self.paths.print_param()
# UI\ -\ Basic\ parameters:1 ends here

# [[file:../Measure_samples.org::src-config-juncture-voltage-class][src-config-juncture-voltage-class]]
#############################################################
## @class   juncture_voltage
#  @brief   All functionality related to the juncture voltage
#
#  @details This class defines the behavior of the jucture
#           voltage. Provides the default values and range
#           plus the corresponding interface.
#############################################################
class juncture_voltage(numerical_parameter):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):
        _dflt = 0.1 # 
        _min = 0.0  #
        _max = 0.3  #
        _name = "Juncture Voltage"
        super(juncture_voltage, self).__init__(_name,_dflt, _min, _max)
# src-config-juncture-voltage-class ends here

# [[file:../Measure_samples.org::src-config-piezo-speed-class][src-config-piezo-speed-class]]
#############################################################
## @class   piezo_speed
#  @brief   All functionality related to the
#           piezo_speed_breaking
#
#  @details This class defines the behavior of the piezo
#           speed voltage relations which is defined in [V/s]
#           Provides the default values and range plus the
#           corresponding interfaces.
#############################################################
class piezo_speed(numerical_parameter):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):
        _dflt = 300.0 #
        _min = 30.0   #
        _max = 300.0  #
        _name = "Piezo Speed"
        super(piezo_speed, self).__init__(_name,_dflt, _min, _max)
        self.fixed_speed = _dflt
# src-config-piezo-speed-class ends here

# [[file:../Measure_samples.org::src-config-traces-class][src-config-traces-class]]
#############################################################
## @class   traces
#  @brief   All functionality related to the number of traces
#
#  @details This class defines the parameter that controls
#           the number of traces (runs) performed using the
#           piezo. Each trace correspond to a full cycle
#           from closed juncture to open and back.
#############################################################
class traces(integer_parameter):
      #############################################################
      ## @brief   Initilaization code
      #############################################################
      def __init__(self):
          _dflt = int(5000)  #
          _min = int(1)      #
          _max = int(20000)  #
          _name = "Number of Traces"
          super(traces, self).__init__(_name,_dflt, _min, _max)
# src-config-traces-class ends here

# [[file:../Measure_samples.org::*Data%20directory][Data\ directory:1]]
#############################################################
## @class   traces
#  @brief   All functionality related to the data directory
#
#  @details This class defines the parameter that controls
#           where the results will be stored. PENDING- TODO
#############################################################
class paths:
    _subdir= "data"#
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):
        self.reset()
    ##############################################################
    ## @brief   restores the default value of the number of traces
    ##############################################################
    def reset(self): #
        fname = inspect.getframeinfo(inspect.currentframe()).filename
        module_path = os.path.dirname(os.path.abspath(fname))
        script_path = os.path.dirname(module_path)
        data_path = os.path.join(script_path,self._subdir)
        self.script_root = script_path
        self.data_dir = data_path
    ## @brief   there is no need to validate?
    def validate(self, new_path):#
        return os.path.isdir(new_path)
    #############################################################
    ## @brief   Updates the piezo speed only if the new
    #           value is within range. Ensures it's an int
    #############################################################
    def update(self,new_path):#
        if self.validate(new_path):
            self.data_dir = new_path
    #############################################################
    ## @brief   Print the parameter.
    #############################################################
    def print_param(self):#
        print("Script Root Directory = %s" % self.script_root)
        print("Data Directory = %s" % self.data_dir)
# Data\ directory:1 ends here

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

# [[file:../Measure_samples.org::gui-config-window][gui-config-window]]
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
# gui-config-window ends here

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

# [[file:../Measure_samples.org::*Basic%20parameters%20layout][Basic\ parameters\ layout:1]]
def ui_basic_param_layout(window):
    basic_params = window.ui_config.config._b_params ## Fix this
    # Num parameters fields
    jv_label, jv_text = num_param_label_textbox(basic_params.juncture)
    ps_label, ps_text = num_param_label_textbox(basic_params.piezo_speed)
    tr_label, tr_text = num_param_label_textbox(basic_params.traces)
    # Change directory dialog and fields
    dir_label = QtGui.QLabel(basic_params.paths.data_dir)
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
# Basic\ parameters\ layout:1 ends here

# [[file:../Measure_samples.org::*Presentation%20parameters%20layout][Presentation\ parameters\ layout:1]]
def ui_adv_param_layout(window):
    return ui_basic_param_layout(window)

def ui_presentation_param_layout(window):
    return ui_basic_param_layout(window)
# Presentation\ parameters\ layout:1 ends here

# [[file:../Measure_samples.org::src-qvalidator-num-param][src-qvalidator-num-param]]
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

# [[file:../Measure_samples.org::*Parameter%20labels][Parameter\ labels:1]]
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
# Parameter\ labels:1 ends here

# [[file:../Measure_samples.org::*Change%20directory%20dialog][Change\ directory\ dialog:1]]
def showDialog(window,dir_label):
    paths = window.ui_config.config._b_params.paths
    fname = QtGui.QFileDialog.getExistingDirectory(window, 'Open file',
            paths.data_dir)
    if(fname):
        paths.update(fname)
        dir_label.setText(paths.data_dir)
        print(paths.data_dir)
# Change\ directory\ dialog:1 ends here
