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
import modules.ui_gui
import modules.utilities as utl
import os
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

############################################################
## @class  CMD
#  @brief  UI calss to encode the possible commands for the
#         program
############################################################
class UI_CMD:
    EXIT    = 0
    M_BREAK = 1
    MEASURE = 2

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

    ## asdf

def ui_get_gui_config():
    retval = modules.ui_gui.run_gui()
    return retval

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

class basic_params:
      def __init__(self):
            self.juncture = juncture_voltage()
            self.piezo_speed = piezo_speed()
            self.traces = traces()
            self.data_dir = data_dir()
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
            self.data_dir.print_param()

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

#############################################################
## @class   traces
#  @brief   All functionality related to the data directory
#
#  @details This class defines the parameter that controls
#           where the results will be stored. Is a string
#           that codifies the directory, depending on the
#           os and inspect modules
#############################################################
class data_dir:
    _subdir= "data"#
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):#
        self.reset()
    ##############################################################
    ## @brief   restores the default value of the number of traces
    ##############################################################
    def reset(self): #
        script_root = utl.get_script_root_path()
        data_path = os.path.join(script_root,self._subdir)
        self.path = data_path
    ##############################################################
    ## @brief   Ensures the new target string is a directory
    ##############################################################
    def validate(self, new_path):#
        return os.path.isdir(new_path)
    #############################################################
    ## @brief   Updates the target directory only if its a
    #           directory in the filesystem
    #############################################################
    def update(self,new_path):#
        if self.validate(new_path):
            self.path = new_path
    #############################################################
    ## @brief   Print the parameter.
    #############################################################
    def print_param(self):#
        print("Data Directory = %s" % self.path)

## asdf

class adv_params:
      def __init__(self):
            self.asdf = 1



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

class presentation:
      def __init__(self):
            self.asdf = 1


