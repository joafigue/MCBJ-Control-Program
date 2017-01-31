# [[file:~/Lab_Diana/Programa_python/MCBJ-Control-Program/Measure_samples.org::*Faulhaber%20testing][Faulhaber testing:1]]
import modules.faulhaber_driver as fh_driver
import pylab as pl
import sys
sys.path.append("../")
from modules.adwin_driver import *
from modules.configuration import *

def stop():
    motor = fh_driver.faulhaber_motor()
    motor.enable_motor()
    motor.stop_motor()
    motor.disable_motor()
    adwin_driver(1, "")


# Configure Plot
infile = "Measurement_deafult_config.yaml"
outfile = "Measurement_read_config.yaml"
config = yaml_build_config_from_file(infile)
dconfig = config.display_config
hconfig = config.hist_config
iv_config = config.iv_config

adw = adwin_iv_driver(iv_config)
adw.start_process()

motor = fh_driver.faulhaber_motor()
print("Motor Pos = {0}".format(motor.get_position()))

motor.enable_motor()
motor.set_target_speed(-2.0)
pl.pause(1)
for count in range(11):
    pl.pause(0.5)
    print(motor.get_position())
    print(adw.get_conductance())

print("speed change")
#pl.pause(5)
motor.set_target_speed(2.0)
for count in range(11):
    pl.pause(0.5)
    print(motor.get_position())
    print(adw.get_conductance())

# motor.move_to(0)

motor.stop_motor()
motor.disable_motor()

stop()
# Faulhaber testing:1 ends here
