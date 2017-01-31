""" Module parameters - Defines configurable parameters and global constants

           This file defines the configurable parameters of the
           program with their corresponding interfaces and
           validations.
           Also the program provides the definitions of the
           global constants of the program
"""
__author__ = "Joaquin Figueroa"

import os
import utilities as utl

#############################################################
## @class   traces
#  @brief   All functionality related to the data directory
#
#  @details This class defines the parameter that controls
#           where the results will be stored. Is a string
#           that codifies the directory, depending on the
#           os and inspect modules
#############################################################
class save_dir(object):
    _subdir= "data"#
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):#
        self.value = None
        self.reset()
    ##############################################################
    ## @brief   restores the default value of the number of traces
    ##############################################################
    def reset(self): #
        script_root = utl.get_script_root_path()
        data_path = os.path.join(script_root, self._subdir)
        self.value = data_path
    ##############################################################
    ## @brief   Ensures the new target string is a directory
    ##############################################################
    def validate(self, new_path):#
        return new_path and os.path.isdir(new_path)
    #############################################################
    ## @brief   Updates the target directory only if its a
    #           directory in the filesystem
    #############################################################
    def update(self, new_path):#
        if self.validate(new_path):
            self.value = new_path
    #############################################################
    ## @brief   Returns the value of the parameter
    #############################################################
    def get_value(self): # 
        return self.value
    #############################################################
    ## @brief   Print the parameter.
    #############################################################
    def print_param(self):#
        print("Data Directory = %s" % self.value)

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
    def __init__(self, name, dflt_val, min_val, max_val):#
        self._dflt = dflt_val
        self._min = min_val
        self._max = max_val
        self.name = name
        self.value = None
        self.reset()
    #############################################################
    ## @brief   restores the default value of the parameter
    #############################################################
    def reset(self): #
        self.value = float(self._dflt)
    #############################################################
    ## @brief   Determines if a new value is in the permited
    #           range
    #############################################################
    def validate(self, val):#
        if val == None:
            return False
        val = float(val)
        return (self._min <= val) & (val <= self._max)
    #############################################################
    ## @brief   Updates the stored value only if the new
    #           value is within range
    #############################################################
    def update(self, new_val):#
        if self.validate(new_val):
            self.value = float(new_val)
    #############################################################
    ## @brief   Updates the stored value only if the new
    #           value is within range, otherwise returns to
    #           the default value
    #############################################################
    def update_or_dflt(self, new_val, verbose=True): #
        if self.validate(new_val):
            self.value = float(new_val)
        else:
            self.reset()
            if verbose:
                self.error_message(new_val)
    #############################################################
    ## @brief   returns the value
    #############################################################
    def get_value(self):        #
        return self.value
    #############################################################
    ## @brief   Prints the parameter name and its value
    #############################################################
    def print_param(self):#
        print("{0} = {1}".format(self.name, self.value))
    #############################################################
    ## @brief   Prints error message if parameter outside range
    #############################################################
    def error_message(self, value):#
        print("------------------------------------------------")
        print("ERROR INVALID PARAMETER VALUE:")
        print("Value {0} is invalid for parameter {1}".format(self.name, value))
        print("Using default value {0}".format(self._dflt))
        print("Valid range for parameter {0} is:".format(self.name))
        print("Range min ={0}, Max ={1}".format(self._min, self._max))
        print("------------------------------------------------")

#############################################################
## @class   Integer Parameter
#  @brief   All functionality related to the numerical
#           parameters that are to be treated as int
#############################################################
class integer_parameter(numerical_parameter):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self, name, dflt_val, min_val, max_val):
        _dflt = int(dflt_val)
        _min = int(min_val)
        _max = int(max_val)
        self.value = None
        super(integer_parameter, self).__init__(name, _dflt, _min, _max)
    #############################################################
    ## @brief   Determines if a new int value is in the permited
    #           range, and integer
    #############################################################
    def validate(self, val): # 
        is_valid = super(integer_parameter, self).validate(val)
        return  val and float(val).is_integer() and is_valid
    #############################################################
    ## @brief   Determines if a new int value is in the permited
    #           range, and integer
    #############################################################
    def update(self, new_val): # 
        super(integer_parameter, self).update(new_val)
        self.value = int(self.value)
    #############################################################
    ## @brief   Determines if a new int value is in the permited
    #           range, and integer
    #############################################################
    def get_value(self): # 
        return int(super(integer_parameter, self).get_value())
    #############################################################
    ## @brief   Prints the parameter name and its value
    #############################################################
    def print_param(self): # 
        print("%s = %d" % (self.name, self.value))

#############################################################
## @class   avg_points
#  @brief   All functionality related to the number of average points
#
#  @details This class defines the behavior of the jucture
#           voltage. Provides the default values and range
#           plus the corresponding interface.
#############################################################
class avg_points(integer_parameter):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):
        _dflt = 32
        _min = 1
        _max = 99
        _name = "Average Points"
        super(avg_points, self).__init__(_name, _dflt, _min, _max)

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
        _dflt = 0.1
        _min = 0.0
        _max = 0.3
        _name = "Juncture Voltage"
        super(juncture_voltage, self).__init__(_name, _dflt, _min, _max)

#############################################################
## @class   piezo_break
#  @brief   All functionality related to the
#           piezo_speed_breaking
#
#  @details This class defines the behavior of the piezo
#           speed voltage relations which is defined in [V/s]
#           Provides the default values and range plus the
#           corresponding interfaces.
#############################################################
class break_speed(numerical_parameter):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):
        _dflt = 300.0
        _min = 10.0
        _max = 900.0
        _name = "Piezo Speed Breaking"
        super(break_speed, self).__init__(_name, _dflt, _min, _max)

#############################################################
## @class   piezo_break
#  @brief   All functionality related to the
#           piezo_speed_breaking
#
#  @details This class defines the behavior of the piezo
#           speed voltage relations which is defined in [V/s]
#           Provides the default values and range plus the
#           corresponding interfaces.
#############################################################
class post_breaking_voltage(numerical_parameter):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):
        _dflt = 200.0
        _min = 1.0
        _max = 999.0
        _name = "Post Breaking Voltage"
        super(post_breaking_voltage, self).__init__(_name, _dflt, _min, _max)

#############################################################
## @class   piezo_make
#  @brief   All functionality related to the
#           piezo_speed_making
#
#  @details This class defines the behavior of the piezo
#           speed voltage relations which is defined in [V/s]
#           Provides the default values and range plus the
#           corresponding interfaces.
#############################################################
class make_speed(numerical_parameter):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):
        _dflt = 500.0
        _min = 30.0
        _max = 990.0
        _name = "Piezo Speed Making"
        super(make_speed, self).__init__(_name, _dflt, _min, _max)

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
        _dflt = int(5000)
        _min = int(1)
        _max = int(20000)
        _name = "Number of Traces"
        super(traces, self).__init__(_name, _dflt, _min, _max)

#############################################################
## @class   Skip_points
#  @brief   All functionality related to
#
#  @details This class defines the parameter that controls
#           the number of traces (runs) performed using the
#           piezo. Each trace correspond to a full cycle
#           from closed juncture to open and back.
#############################################################
class skip_points(integer_parameter):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):
        _dflt = int(10)
        _min = int(1)
        _max = int(99)
        _name = "Points to skip/not save in Adwin"
        super(skip_points, self).__init__(_name, _dflt, _min, _max)

#############################################################
## @class   display_xmin
#  @brief   All functionality related to the minimum of X axis
#
#  @details This class defines the behavior of the minimum
#           for the X axis. Provides the default values and range
#           plus the corresponding interface.
#############################################################
class display_xmin(numerical_parameter):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):
        _dflt = -0.5
        _min = -0.9
        _max = -0.1
        _name = "display_xmin"
        super(display_xmin, self).__init__(_name, _dflt, _min, _max)

#############################################################
## @class   display_xmax
#  @brief   All functionality related to the maximum of X axis
#
#  @details This class defines the behavior of the maximum
#           for the X axis. Provides the default values and range
#           plus the corresponding interface.
#############################################################
class display_xmax(numerical_parameter):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):
        _dflt = 2
        _min = 0.9
        _max = 3.9
        _name = "display_xmax"
        super(display_xmax, self).__init__(_name, _dflt, _min, _max)

#############################################################
## @class   display_Gmin
#  @brief   All functionality related to the minimum of Y axis
#
#  @details This class defines the behavior of the minimum
#           for the Y axis. Provides the default values and range
#           plus the corresponding interface.
#############################################################
class display_Gmin(numerical_parameter):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):
        _dflt = 1e-7
        _min = 1e-9
        _max = 1e-6
        _name = "display_Gmin"
        super(display_Gmin, self).__init__(_name, _dflt, _min, _max)

#############################################################
## @class   display_xmax
#  @brief   All functionality related to the maximum of Y axis
#
#  @details This class defines the behavior of the maximum
#           for the X axis. Provides the default values and range
#           plus the corresponding interface.
#############################################################
class display_Gmax(numerical_parameter):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):
        _dflt = 10
        _min = 1
        _max = 100
        _name = "display_Gmax"
        super(display_Gmax, self).__init__(_name, _dflt, _min, _max)

#############################################################
## @class   display_nXbins
#  @brief   All functionality related to the X axis slots(bins)
#
#  @details This class defines the behavior of the number of
#           slots for the X axis. Provides the default value
#           and range plus the corresponding interface.
#############################################################
class display_nXbins(integer_parameter):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):
        _dflt = 161
        _min = 99
        _max = 999
        _name = "display_nDbins"
        super(display_nXbins, self).__init__(_name, _dflt, _min, _max)

#############################################################
## @class   display_nGbins
#  @brief   All functionality related to the Y axis slots(bins)
#
#  @details This class defines the behavior of the number of
#           slotsfor the Y axis. Provides the default value
#           and range plus the corresponding interface.
#############################################################
class display_nGbins(integer_parameter):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):
        _dflt = 251
        _min = 99
        _max = 999
        _name = "display_nGbins"
        super(display_nGbins, self).__init__(_name, _dflt, _min, _max)

#############################################################
## @class   bool_param
#  @brief   Defines the generic boolean parameter and interface
#
#  @details This class defines generic parameters, in order
#           to allow for extension to all boollean parameters
#           This class provides with the common features to
#           all boolean parameters
#############################################################
class bool_param(object):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self, name, dflt=True):#(ref:src-bool-init)
        self._dflt = dflt
        self.name = name
        self.value = None
        self.reset()
    ##############################################################
    ## @brief   restores the default value of the number of traces
    ##############################################################
    def reset(self): #(ref:src-bool-reset)
        self.value = self._dflt
    ##############################################################
    ## @brief   Ensures the new target string is a directory
    ##############################################################
    def validate(self, new_value):#(ref:src-bool-validation)
        return type(new_value) is bool
    #############################################################
    ## @brief   Updates the target directory only if its a
    #           directory in the filesystem
    #############################################################
    def update(self, new_value):#(ref:src-bool-update)
        if self.validate(new_value):
            self.value = new_value
    #############################################################
    ## @brief   Returns the value of the parameter
    #############################################################
    def get_value(self): # (ref:src-bool-value)
        return self.value
    #############################################################
    ## @brief   Updates the stored value only if the new
    #           value is within range, otherwise returns to
    #           the default value
    #############################################################
    def update_or_dflt(self, new_val): #(ref:src-np-update-dflt)
        if self.validate(new_val):
            self.value = new_val
        else:
            self.reset()
    #############################################################
    ## @brief   Print the parameter.
    #############################################################
    def print_param(self):#(ref:src-bool-print)
        print("{0} is = {1}".format(self.name, self.value))

#############################################################
## @class   save_data
#  @brief   All functionality to the decition to save data
#
#  @details This class defines the parameter that controls
#           if the data is stored
#           that codifies the directory, depending on the
#           os and inspect modules
#############################################################
class save_data(bool_param):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):
        name = "Save Data"
        super(save_data, self).__init__(name)

#############################################################
## @class   Use Json
#  @brief   Basically allow to turn of the motor. Used in IV
#############################################################
class use_json(bool_param):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):
        name = "Use Json for Write data"
        super(use_json, self).__init__(name, False)

#############################################################
## @class   use_log_amp
#  @brief   All functionality to the decition to save data
#
#  @details This class defines the parameter that controls
#           if the logartimic amplifier is used
#############################################################
class use_log_amp(bool_param):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):
        name = "Use Logaritmic amplifier"
        super(use_log_amp, self).__init__(name)

#############################################################
## @class   move_motor
#  @brief   Basically allow to turn of the motor. Used in IV
#############################################################
class iv_move_motor(bool_param):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self):
        name = "Move motor during IV"
        super(iv_move_motor, self).__init__(name)

# Non configurable parameters
class GLOBAL_CONSTANTS(object):
    G0 = 7.74809173e-5          # Quantum Conductance
    start_jv = 0
    end_jv = 0
    IV_settling_time = 10       # ms
    IV_max_data_points = 50000000

class adwin_log_amplifier(object):
    def __init__(self):
        calibration_dir = ADW_GCONST.PROGRAM_DIR
        root_path = utl.get_script_root_path()
        program_path = os.path.join(root_path, calibration_dir)
        filename = "calibrationIO.txt"
        calibration_file = os.path.join(program_path, filename)
        if (os.path.isfile(calibration_file)):
            self.read_data_file(calibration_file)
        else:
            raise Exception("Bad file, check %s" %calibration_file)
    def read_data_file(self, filename):
        # reads matrix from data file. As optional input a column can be specified
        data=[]
        my_file = open(filename)
        for line in my_file:
            line_list = [float(x) for x in line.split()]
            data.append(line_list)
        self.data = data
    def get_calibration(self, Column=2):
        data = self.data
        retlist = []
        for i in range(len(data)):
            retlist.append(data[i][Column])
        return retlist

class MB_CONST(object):
    BROKEN_CONDUCTANCE = 1e-6   # IN G0
    RESTORE_CONDUCTANCE = 50    # in G0
    BREAK_SPEED = -2            # In us
    MAKE_SPEED = 2              # in us

# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::*Adwin%20driver-global%20constants][Adwin driver-global constants:1]]
###########################################################################
## @class  ADW_GCONST
#  @brief  Parameters for Adwin instrument
#
#  @details This is the list of parameters used by the ADwin
#           ADDRESS -> Communication address with the ADwin
#           BOOT_SCRIPT_DFLT -> Where is the operative system
#           PROGRAM_DIR -> The directory where all adwin files are stored
#           HIGH_PERIOD -> high priority process clock period (25 ns)
#           OUTPUT_RANGE -> Output voltage in volts (+- 10 v)
#           RESOLUTION -> 16 bits of representation for continuous values
#           IV_PROCESS -> IV measurements program stored in slot 1
#           HIST_PROCESS -> Histogram program stored in slot 2
#           PROCESS_DELAY -> number of ADwin clock between each operation
#                            set to 400, in order to operate every 10 us
###########################################################################
class ADW_GCONST(object):
    # Interface with computer
    ADDRESS = 0x150
    BOOT_SCRIPT_DFLT = 'C:\ADwin\ADwin9.btl'
    PROGRAM_DIR = "adwin_programs"
    # Adwin instrument characterization
    HIGH_PERIOD      = 25e-9
    OUTPUT_RANGE     = 10.0
    OUTPUT_MAX_D     = 15.0
    RESOLUTION       = 16.0
    # Program Constants
    PROCESS_DELAY    = 400
# Adwin driver-global constants:1 ends here

# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::src-faulhaber-constants][src-faulhaber-constants]]
#################################################################
## @author  Joaquin Figueroa
#  @brief   Constants used for the faulhaber interface
#
#  @details These are the constants used by the faulhaber
#           interface.
#################################################################
class FH_CONST(object):
    PORT = "COM3" #
    BAUD_RATE = 9600 #
    PITCH = 150 #
    GEARBOX = 246 #
    MAX_POS = 5000000#
    MIN_POS = -7000000#
    MAX_SPEED = 800#in RPM
    MAX_ACCEL = 40#in RPM/s
# src-faulhaber-constants ends here
