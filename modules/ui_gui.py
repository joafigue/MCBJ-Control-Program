""" Module ui_gui - Provides the GUI for configuring the experiment

           This file provides a GUI for the user to be able to
           configure the experiment and run it.
"""
__author__ = "Joaquin Figueroa"

from PyQt4 import QtGui
from PyQt4 import QtCore
import modules.configuration as conf

############################################################
## @brief   Runs the GUI for the program
############################################################
def run_gui():
    app = QtGui.QApplication([]) # Create "aplication"
    config_window = ui_config_window() # Instantiate widget
    app.exec_()                        # Execute appliaction
    return config_window.ui_config, config_window.config

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
        self.ui_config = gui_cmd()
        self.config = conf.program_config() #
        buttons_layout = ui_create_buttons_layout(self) #
        config_layout  = ui_create_config_layout(self)  #
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(config_layout)
        vbox.addLayout(buttons_layout)

        self.setLayout(vbox)
        self.setGeometry(150, 150, 550, 550)
        self.setWindowTitle('Buttons')
        self.show()

    ############################################################
    ## @brief   Interface to close the window and excecute a
    #           command
    ############################################################
    def close_with_cmd(self, cmd): #
        self.ui_config.update_cmd(cmd)
        self.close()

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
    no_op_button = QtGui.QPushButton("Diagnose Experimental Setup")
    no_op_button.clicked.connect(
        lambda: widget.close_with_cmd(UI_CMD.NO_OP_PLOT))
    no_op_button.setToolTip("Continuous G measure. Use for experiment Diagnosis")
    # Measure Button
    measure_button = QtGui.QPushButton("Perform Measurement")
    measure_button.clicked.connect(
        lambda: widget.close_with_cmd(UI_CMD.MEASURE))
    measure_button.setToolTip(
        "Performs measurement using the motor and piezo")

    # Build Layout
    hbox = QtGui.QHBoxLayout()
    hbox.addStretch(1)
    hbox.addWidget(quit_button)
    hbox.addWidget(no_op_button)
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
def ui_create_config_layout(ui_window):
    # Define each group layout
    iv_param_layout = ui_iv_param_layout(ui_window)
    hist_param_layout = ui_hist_param_layout(ui_window)
    display_param_layout = ui_display_param_layout(ui_window)
    save_opts_layout = ui_save_opts_layout(ui_window)
    # Define the labels
    iv_label = QtGui.QLabel("---- Adwin IV-measurement Parameters ----")
    hist_label = QtGui.QLabel("---- Adwin histogram Parameters ----")
    display_label = QtGui.QLabel("---- Adwin display Parameters ----")
    save_label = QtGui.QLabel("---- Save Options  ----")
    # Configure the layout
    vbox = QtGui.QVBoxLayout()
    vbox.addStretch(1)
    vbox.addWidget(iv_label)
    vbox.addLayout(iv_param_layout)
    vbox.addWidget(hist_label)
    vbox.addLayout(hist_param_layout)
    vbox.addWidget(display_label)
    vbox.addLayout(display_param_layout)
    vbox.addWidget(save_label)
    vbox.addLayout(save_opts_layout)
    return vbox

def ui_iv_param_layout(window):
    iv_params = window.config.iv_config
    # Num parameters fields
    jv_label, jv_text = num_param_label_textbox(iv_params.measure_jv)
    avg_label, avg_text = num_param_label_textbox(iv_params.avg_points)
    log_cb = boolean_parameter_checkbox(iv_params.use_log_amp)
    motor_cb = boolean_parameter_checkbox(iv_params.move_motor)

    # Add fields to the layout
    grid = QtGui.QGridLayout()

    grid.setSpacing(10)

    grid.addWidget(jv_label, 1, 0)
    grid.addWidget(jv_text, 1, 1)

    grid.addWidget(avg_label, 2, 0)
    grid.addWidget(avg_text, 2, 1)

    grid.addWidget(log_cb, 3, 0)
    grid.addWidget(motor_cb, 3, 1)

    return grid

def ui_hist_param_layout(window):
    hist_params = window.config.hist_config
    # Num parameters fields
    jv_label, jv_text = num_param_label_textbox(hist_params.measure_jv)
    avg_label, avg_text = num_param_label_textbox(hist_params.avg_points)
    skip_label, skip_text = num_param_label_textbox(hist_params.skip)
    brk_label, brk_text = num_param_label_textbox(hist_params.break_speed)
    post_label, post_text = num_param_label_textbox(hist_params.post_breaking_v)
    mk_label, mk_text = num_param_label_textbox(hist_params.make_speed)
    cb = boolean_parameter_checkbox(hist_params.use_log_amp)

    # Add fields to the layout
    grid = QtGui.QGridLayout()
    grid.setSpacing(10)

    grid.addWidget(jv_label, 1, 0)
    grid.addWidget(jv_text, 1, 1)

    grid.addWidget(avg_label, 2, 0)
    grid.addWidget(avg_text, 2, 1)

    grid.addWidget(brk_label, 3, 0)
    grid.addWidget(brk_text, 3, 1)

    grid.addWidget(post_label, 4, 0)
    grid.addWidget(post_text, 4, 1)

    grid.addWidget(mk_label, 5, 0)
    grid.addWidget(mk_text, 5, 1)

    grid.addWidget(skip_label, 6, 0)
    grid.addWidget(skip_text, 6, 1)

    grid.addWidget(cb, 7, 0)

    return grid

def ui_display_param_layout(window):
    display_params = window.config.display_config
    # Num parameters fields
    xmin_label, xmin_text = num_param_label_textbox(display_params.xmin)
    xmax_label, xmax_text = num_param_label_textbox(display_params.xmax)
    Gmin_label, Gmin_text = num_param_label_textbox(display_params.Gmin)
    Gmax_label, Gmax_text = num_param_label_textbox(display_params.Gmax)

    nGbins_label, nGbins_text = num_param_label_textbox(display_params.nGbins)
    nXbins_label, nXbins_text = num_param_label_textbox(display_params.nXbins)

    # Add fields to the layout
    grid = QtGui.QGridLayout()
    grid.setSpacing(10)

    grid.addWidget(xmin_label, 1, 0)
    grid.addWidget(xmin_text, 1, 1)

    grid.addWidget(xmax_label, 2, 0)
    grid.addWidget(xmax_text, 2, 1)

    grid.addWidget(Gmin_label, 3, 0)
    grid.addWidget(Gmin_text, 3, 1)

    grid.addWidget(Gmax_label, 4, 0)
    grid.addWidget(Gmax_text, 4, 1)


    grid.addWidget(nGbins_label, 5, 0)
    grid.addWidget(nGbins_text, 5, 1)

    grid.addWidget(nXbins_label, 6, 0)
    grid.addWidget(nXbins_text, 6, 1)


    return grid

def ui_save_opts_layout(window):
    save_opts = window.config.save_config

    # Change directory dialog and fields
    dir_label = QtGui.QLabel(save_opts.save_dir.get_value())
    dir_btn = QtGui.QPushButton('Change Directory')
    dir_btn.clicked.connect(lambda: showDialog(window, save_opts, dir_label))
    traces_label, traces_text = num_param_label_textbox(save_opts.traces)

    save_cb = boolean_parameter_checkbox(save_opts.save_data)

    json_cb = boolean_parameter_checkbox(save_opts.use_json)

    # Add fields to the layout
    grid = QtGui.QGridLayout()
    grid.setSpacing(10)


    grid.addWidget(traces_label, 1, 0)
    grid.addWidget(traces_text, 1, 1)

    grid.addWidget(dir_label, 2, 0)
    grid.addWidget(dir_btn, 2, 1)

    grid.addWidget(save_cb, 3, 0)
    grid.addWidget(json_cb, 3, 1)

    return grid

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

#############################################################
## @brief   Creates a label and textbox for a numerical
#           parameter.
#############################################################
def num_param_label_textbox(parameter):
    label = QtGui.QLabel(parameter.name)
    textbox = QtGui.QLineEdit()
    param_validator = QValidator_num_param(parameter)
    textbox.setValidator(param_validator)
    textbox.setText(str(parameter.get_value()))
    return (label, textbox)

def boolean_parameter_checkbox(parameter):
    label = parameter.name
    cb = QtGui.QCheckBox(label)
    if parameter.get_value():
        cb.toggle()
    cb.stateChanged.connect(
        lambda: parameter.update(cb.isChecked()))

    return cb

def showDialog(window, save_opts, dir_label):
    save_dir = save_opts.save_dir
    fname = QtGui.QFileDialog.getExistingDirectory(window, 'Open file',
                                                   save_dir.get_value())
    if(fname):
        save_dir.update(str(fname))
        dir_label.setText(save_dir.get_value())
        print(save_dir.get_value())

############################################################
## @class  CMD
#  @brief  UI calss to encode the possible commands for the
#         program
############################################################
class UI_CMD(object):
    EXIT    = 0
    NO_OP_PLOT = 1
    MEASURE = 2

class gui_cmd(object):
    def __init__(self):
        self.cmd = UI_CMD.EXIT
    def update_cmd(self, cmd):
        self.cmd = cmd
