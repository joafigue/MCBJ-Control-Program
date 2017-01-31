# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::*Adwin%20driver-header][Adwin driver-header:1]]
""" Module adwin_driver -  Provides the interfaces for the Adwin
           This file provides  the Adwin interface,
           which defines high and low level functionalities.
           The user should use onlythe high level functionality
           if possible.
"""
__author__ = "Joaquin Figueroa"


import os
import numpy as np
import pylab as pl
import ADwin
import utilities as utl
import parameters as param
# Adwin driver-header:1 ends here

# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::*Adwin%20driver-base%20class%20Interface][Adwin driver-base class Interface:1]]
############################################################
## @class   adwin_driver
#  @details This class initializes the driver without
#           any particular purpose. This is the parent class
#           and user should use this only when designing a
#           new measurement method
############################################################
class adwin_driver(object):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self, process_number, process_file):
        self._adwin_subdir= param.ADW_GCONST.PROGRAM_DIR
        self.adw = ADwin.ADwin(param.ADW_GCONST.ADDRESS, 1)
        self.adw.Boot(param.ADW_GCONST.BOOT_SCRIPT_DFLT)
        self.process_number = process_number
        self.filename = process_file
    #############################################################
    ## @brief   Load the measurement program. Basic interface
    #############################################################
    def load_process(self):
        filename = self.filename
        root_path = utl.get_script_root_path()
        program_path = os.path.join(root_path, self._adwin_subdir)
        process_file = os.path.join(program_path, filename)
        if (os.path.isfile(process_file)):
            self.adw.Load_Process(process_file)
        else:
            raise Exception("Bad file, check %s" %process_file)
    #############################################################
    ## @brief   Starts the measurement process
    #############################################################
    def start_process(self):
        self.adw.Start_Process(self.process_number)
    #############################################################
    ## @brief   Stop the measurement process
    #############################################################
    def stop_process(self):
        self.adw.Stop_Process(self.process_number)
    #############################################################
    ## @brief   Show information on the adwin and process
    #############################################################
    def analyze(self):
        version = self.adw.Test_Version()
        processor = self.adw.Processor_Type()
        print("Version {0}".format(version))
        print("Processor type: {0}".format(processor))
        self.print_status()
    #############################################################
    ## @brief   Minor utility to print the status information
    #############################################################
    def print_status(self):
        process_number = self.process_number
        status = self.adw.Process_Status(process_number)
        if (status == 0):
            print("Process {0} is not running".format(process_number))
        if status == 1:
            print("Process {0} is running".format(process_number))
        if status < 0:
            print("Process {0} is stopped".format(process_number))
# Adwin driver-base class Interface:1 ends here

# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::src-adwin-parameters][src-adwin-parameters]]
class ADW_IV_CONST(object):
    PROCESS_NUMBER = 1
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::src-adwin-iv-param][src-adwin-iv-param]]
    ###########################################################################
    ## @brief  Indices  for int vars in ADwin used for IV measurements
    ###########################################################################
    # Inputs for the ADWIN IV measurement
    START_JV    = 1
    MEASURE_JV  = 2
    END_JV      = 3
    WAIT        = 7
    AVG         = 8
    MAX_DATA    = 10
    # outputs for the ADWIN IV measurement
    END_STATUS  = 12
    # src-adwin-iv-param ends here
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::src-adwin-iv-fparam][src-adwin-iv-fparam]]
    ###########################################################################
    ## @brief  Indices  for float vars in ADwin used for IV measurements.
    ###########################################################################
    # output variables for measured currents for the ADWIN IV measurement
    I_CH1       = 1
    I_CH1_AMPL  = 2
    I_CH2       = 3
    I_CH2_AMPL  = 4
    # src-adwin-iv-fparam ends here
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::src-adwin-iv-aparam][src-adwin-iv-aparam]]
    ###########################################################################
    ## @brief  Indices  for array vars in ADwin used for IV measurements
    ###########################################################################
    # ----------------------------- inputs  ------------------------------
    LOG_AMPL  = 10
    # src-adwin-iv-aparam ends here
# src-adwin-parameters ends here

# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::src-adwin-driver-iv-interface][src-adwin-driver-iv-interface]]
############################################################
## @class   adwin_iv_driver
#  @details This class initializes the driver with the
#           the purpose of performing continuos IV
#           measurements.
#           The class provides the interfaces to extract
#           the data as necesary
############################################################
class adwin_iv_driver(adwin_driver):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self, config):
        process_number = ADW_IV_CONST.PROCESS_NUMBER
        filename = "iv_measurement_process.T9{0}".format(process_number)
        super(adwin_iv_driver, self).__init__(process_number, filename)
        self.config = config
        self.load_process()
        self.configure_process()
    #############################################################
    ## @brief   Set all parameters to start measuring
    #############################################################
    def configure_process(self): #  (ref:adw-iv-configure)
        c = self.config
        log_array = c.get_log_array()
        length = len(log_array)
        self.adw.Set_Processdelay(ADW_IV_CONST.PROCESS_NUMBER,
                                  param.ADW_GCONST.PROCESS_DELAY )
        self.adw.Set_Par(ADW_IV_CONST.START_JV, c.get_start_jv())
        self.adw.Set_Par(ADW_IV_CONST.MEASURE_JV, c.get_measure_jv())
        self.adw.Set_Par(ADW_IV_CONST.END_JV, c.get_end_jv())
        self.adw.Set_Par(ADW_IV_CONST.WAIT, c.get_wait_cycles())
        self.adw.Set_Par(ADW_IV_CONST.AVG, c.get_avg_points())
        self.adw.Set_Par(ADW_IV_CONST.MAX_DATA, c.get_max_data())
        self.adw.SetData_Float(log_array,
                              ADW_IV_CONST.LOG_AMPL, 1, length)
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::src-adwin-iv-driver-api][src-adwin-iv-driver-api]]
    #############################################################
    ## @brief   Return the current measured by the ADwin
    #############################################################
    def get_current(self):
        if self.config.get_use_log_amp():
            current = self.adw.Get_FPar(ADW_IV_CONST.I_CH1_AMPL)
        else:
            digital_current = self.adw.Get_FPar(ADW_IV_CONST.I_CH1)
            current = adwin_DAC(digital_current) /self.config.linear_gain
        return current
    #############################################################
    ## @brief   Return the conductance measured by the ADwin
    #############################################################
    def get_real_conductance(self):
        return self.get_current()/self.config.get_real_jv()
    #############################################################
    ## @brief   Return the conductance as a "G0" factor measured
    #############################################################
    def get_conductance(self):
        return self.get_real_conductance()/param.GLOBAL_CONSTANTS.G0
    # src-adwin-iv-driver-api ends here
# src-adwin-driver-iv-interface ends here

# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::*Adwin%20driver-histogram%20parameters][Adwin driver-histogram parameters:1]]
class ADW_HIST_CONST(object):
    PROCESS_NUMBER = 2
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::src-adwin-hist-param][src-adwin-hist-param]]
    ###########################################################################
    ## @brief  Indices  for int vars with ADwin for IV measurements
    ###########################################################################
    # Inputs for the ADWIN histogram measurement
    START_JV    = 1
    MEASURE_JV  = 2
    END_JV      = 3
    BREAK_WAIT  = 17
    POST_BREAK_WAIT  = 27
    MAKE_WAIT   = 18
    AVG         = 19
    SKIP        = 30
    # outputs for the ADWIN histogram measurement
    PROCESS_STATUS  = 12
    END_STATUS  = 13
    ERROR_STATUS  = 14
    BREAK_IDX   = 20
    MAKE_IDX    = 21
    # src-adwin-hist-param ends here
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::src-adwin-hist-fparam][src-adwin-hist-fparam]]
    ###########################################################################
    ## @brief  Indices  for float vars with ADwin for IV measurements
    ###########################################################################
    # inputs for the ADWIN histogram measurement
    I_MID_BRK  = 9
    I_MIN_BRK  = 10
    I_MAX_MK   = 11
    # src-adwin-hist-fparam ends here
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::src-adwin-hist-aparam][src-adwin-hist-aparam]]
    ###########################################################################
    ## @brief  Indices  for array vars with ADwin for IV measurements
    ###########################################################################
    # Inputs for the ADWIN histogram measurement
    LOG_AMPL  = 10
    # Outputs for the ADWIN histogram measurement. Histogram
    BRK_HIST  = 1
    BRK_VOLT  = 2
    MK_HIST   = 3
    MK_VOLT   = 4
    # src-adwin-hist-aparam ends here
# Adwin driver-histogram parameters:1 ends here

# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::src-adwin-hist-driver-init][src-adwin-hist-driver-init]]
############################################################
## @class   adwin_hist_driver
#  @details This class initializes the driver with the
#           the purpose of performing histogram
#           measurements.
#           The class provides the interfaces to extract
#           the data as necesary
############################################################
class adwin_hist_driver(adwin_driver):
    #############################################################
    ## @brief   Initilaization code
    #############################################################
    def __init__(self, config):
        process_number = ADW_HIST_CONST.PROCESS_NUMBER
        filename = "hist_measurement_process.T9{0}".format(process_number)
        super(adwin_hist_driver, self).__init__(process_number, filename)
        self.config = config
        self.load_process()
        self.configure_process()
    #############################################################
    ## @brief   Set all parameters to start measuring
    #############################################################
    def configure_process(self): #  (ref:adw-hist-configure)
        c = self.config
        log_array = c.get_log_array()
        length = len(log_array)
        self.adw.Set_Processdelay(ADW_HIST_CONST.PROCESS_NUMBER,
                                  param.ADW_GCONST.PROCESS_DELAY )
        self.adw.Set_Par(ADW_HIST_CONST.START_JV, c.get_start_jv())
        self.adw.Set_Par(ADW_HIST_CONST.MEASURE_JV, c.get_measure_jv())
        self.adw.Set_Par(ADW_HIST_CONST.END_JV, c.get_end_jv())
        self.adw.Set_Par(ADW_HIST_CONST.AVG, c.get_avg_points())
        self.adw.Set_Par(ADW_HIST_CONST.BREAK_WAIT, c.get_break_wait())
        self.adw.Set_Par(ADW_HIST_CONST.POST_BREAK_WAIT, c.get_post_break_wait())
        self.adw.Set_Par(ADW_HIST_CONST.MAKE_WAIT, c.get_make_wait())
        self.adw.Set_Par(ADW_HIST_CONST.SKIP, c.get_skip_points())
        self.adw.Set_FPar(ADW_HIST_CONST.I_MIN_BRK, c.get_I_break_end())
        self.adw.Set_FPar(ADW_HIST_CONST.I_MID_BRK, c.get_I_break_mid())
        self.adw.Set_FPar(ADW_HIST_CONST.I_MAX_MK, c.get_I_make_end()) #
        self.adw.SetData_Float(log_array,
                              ADW_HIST_CONST.LOG_AMPL, 1, length)
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::src-adwin-hist-driver-api][src-adwin-hist-driver-api]]
    def measure_and_get_histogram(self, trace=1):
        self.start_process()
        while self.process_running():
            state = self.adw.Get_Par(ADW_HIST_CONST.PROCESS_STATUS)
            os.system('cls')
            if state == 1:
                print("Run number: {0} \nbreaking 1".format(trace))
            if state == 2:
                print("Run number: {0} \nmaking 1".format(trace))
            pl.pause(0.1)
        self.stop_process()
        break_histogram = self.get_break_histogram()
        make_histogram = self.get_make_histogram()
    
        return break_histogram, make_histogram
    
    
    def get_break_histogram(self):
        break_conductance = self.get_break_conductance()
        break_voltage = self.get_break_voltage()
        return adwin_histogram(break_conductance, break_voltage)
    
    def get_break_conductance(self):
        G0 = self.config.G0
        real_jv = self.config.get_real_jv()
        length = self.adw.Get_Par(ADW_HIST_CONST.BREAK_IDX) -1
        current_hist = self.adw.GetData_Float(ADW_HIST_CONST.BRK_HIST, 1, length)
        current_hist = np.asarray(current_hist)
        conductance_hist = current_hist/(real_jv * G0)
        return conductance_hist
    
    def get_break_voltage(self):
        length = self.adw.Get_Par(ADW_HIST_CONST.BREAK_IDX) -1
        voltage_hist = self.adw.GetData_Float(ADW_HIST_CONST.BRK_VOLT, 1, length)
        voltage_hist = np.asarray(voltage_hist)
        new_voltage_hist = adwin_DAC(voltage_hist)
        return new_voltage_hist
    
    def get_make_histogram(self):
        make_conductance = self.get_make_conductance()
        make_voltage = self.get_make_voltage()
        return adwin_histogram(make_conductance, make_voltage)
    
    def get_make_conductance(self):
        G0 = self.config.G0
        real_jv = self.config.get_real_jv()
        length = self.adw.Get_Par(ADW_HIST_CONST.MAKE_IDX) -1
        current_hist = self.adw.GetData_Float(ADW_HIST_CONST.MK_HIST, 1, length)
        current_hist = np.asarray(current_hist)
        conductance_hist = current_hist/(real_jv * G0)
        return conductance_hist
    
    def get_make_voltage(self):
        length = self.adw.Get_Par(ADW_HIST_CONST.MAKE_IDX) -1
        voltage_hist = self.adw.GetData_Float(ADW_HIST_CONST.MK_VOLT, 1, length)
        voltage_hist = np.asarray(voltage_hist)
        new_voltage_hist = adwin_DAC(voltage_hist)
        return new_voltage_hist
    
    def process_running(self):
        return self.adw.Get_Par(ADW_HIST_CONST.END_STATUS) != 1
    def successful_measurement(self):
        return self.adw.Get_Par(ADW_HIST_CONST.ERROR_STATUS) == 0
    def error_in_breaking(self):
        return self.adw.Get_Par(ADW_HIST_CONST.ERROR_STATUS) & 1 == 1
    def error_in_making(self):
        return (self.adw.Get_Par(ADW_HIST_CONST.ERROR_STATUS) >> 1) & 1 == 1
    
    # src-adwin-hist-driver-api ends here
# src-adwin-hist-driver-init ends here

# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::src-adwin-hist-driver-aux-histogram][src-adwin-hist-driver-aux-histogram]]
class adwin_histogram(object):
    def __init__(self, conductance, voltage):
        self.conductance = conductance
        self.voltage = voltage
        self.length = min(len(self.conductance), len(self.voltage))
    def get_conductance(self):
        return self.conductance
    def get_voltage(self):
        return self.voltage
    def get_voltage_conductance_pair(self, idx):
        return self.conductance[idx], self.voltage[idx]
    def print_histogram(self):
        for idx in range(self.length):
            G, V = self.get_voltage_conductance_pair(idx)
            print("Index = {0}, G = {1}, V = {2}".format(idx, G,V))
# src-adwin-hist-driver-aux-histogram ends here

# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::*Adwin%20converters][Adwin converters:1]]
# This works with numpy array.
def adwin_ADC(analog_value):
    # converts ADC/DAC voltage to bin number, given the voltage range and the param.ADW_GCONST.RESOLUTION as int (adwin digitia representation
    o_range = param.ADW_GCONST.OUTPUT_RANGE
    step=2*o_range/(2**param.ADW_GCONST.RESOLUTION-1)
    zero_v = o_range/step
    restricted = np.maximum(np.minimum(analog_value, o_range), -o_range)
    digital_value = np.asarray(restricted/step + zero_v, dtype=int)
    if digital_value.ndim == 0 or len(digital_value) < 2:
        digital_value = int(digital_value)
    return digital_value

# This works with numpy array.
def adwin_DAC(digital_value):
    # converts ADC/DAC bins to voltage, given the voltage range and the resolution (in bits)
    step = 2 * param.ADW_GCONST.OUTPUT_RANGE / (2**param.ADW_GCONST.RESOLUTION-1)
    # voltage is array of analog/idx conversion
    zero_v = param.ADW_GCONST.OUTPUT_RANGE/step
    analog_value = np.asarray((digital_value - zero_v)*step)
    if analog_value.ndim == 0 or len(analog_value) < 2:
        analog_value = float(analog_value)
    return analog_value

def aux_convert_vps_to_cycles(vps):
    # VPS -> VOltage Per Second
    # We are taking 0->1000 to 0->10, because that's the Adwin range
    voltage_steps = adwin_ADC(vps/100) # in V/seg
    zero_v_steps = adwin_ADC(0)        # in V/seg (for range)
    voltage_steps_seg = voltage_steps - zero_v_steps # in seg
    voltage_steps_ms = voltage_steps_seg * 1e-3

    voltage_wait = 1/voltage_steps_ms # in ms
    return adwin_convert_ms_to_cycles(voltage_wait)

def adwin_convert_ms_to_cycles(time_ms):
    # Stabilization cycles before starting measurement
    # Wait is in ms, but we need to wait number of cycles.
    # Each cycle is 10 us (in seg) => seg
    cycle_time = param.ADW_GCONST.HIGH_PERIOD * param.ADW_GCONST.PROCESS_DELAY
    time_seg = time_ms * 1e-3
    wait_cycles = int(time_seg /cycle_time ) # Because ms
    return wait_cycles
# Adwin converters:1 ends here

# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::*Adwin%20reset][Adwin reset:1]]
def ADwin_stop():
    """ create a new adwin drive, which will reboot the Adwin, and stop all executions"""
    adwin_driver(1, "")            # This reboots the Adwin, killing the process
# Adwin reset:1 ends here
