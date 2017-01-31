import pylab as pl
import time
import os
import sys
sys.path.append("../")
import modules.adwin_driver as adw
import modules.faulhaber_driver as fh
import modules.utilities as utl
import modules.configuration as conf
import modules.parameters as param
import modules.motor_break as mb

def stop():
    motor = fh.faulhaber_motor()
    motor.enable_motor()
    motor.stop_motor()
    motor.disable_motor()
    adw.adwin_driver(1, "")


# Configure Plot
infile = "Measurement_deafult_config.yaml"
outfile = "Measurement_read_config.yaml"
config = conf.yaml_build_config_from_file(infile)
dconfig = config.display_config
hconfig = config.hist_config
iv_config = config.iv_config

motor = fh.faulhaber_motor()
mb.motor_break_print_plot(iv_config)
#mb.motor_break_print(motor, iv_config)
