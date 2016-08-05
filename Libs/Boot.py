###################################
## Driver written by M.L. Perrin ##
## contact: m.l.perrin@tudelft.nl #
###################################

##### IMPORT MODULES #####
import os
import ADwin
import ctypes
import serial
from math import log10
from time import *
from visa import *
os.system('cls')

#from matplotlib import animation

##### LOAD DRIVERS #####
execfile('C:/Users/Usuario/Desktop/Programas (Por ordenar)/python programs/Ignacio/New Setup/Libs/Functions.py')
execfile('C:/Users/Usuario/Desktop/Programas (Por ordenar)/python programs/Ignacio/New Setup/Libs/ADwin_driver.py')
execfile('C:/Users/Usuario/Desktop/Programas (Por ordenar)/python programs/Ignacio/New Setup/Libs/Faulhaber_driver.py')
execfile('C:/Users/Usuario/Desktop/Programas (Por ordenar)/python programs/Ignacio/New Setup/Libs/Measurement_routines.py')
execfile('C:/Users/Usuario/Desktop/Programas (Por ordenar)/python programs/Ignacio/New Setup/Libs/data_processing.py')

##### GENERAL SETTINGS #####
output_range = 10.0                                        # AO1 output range
input_range = 2.5                                          # AI1 input range
log = 1                                                    # logarithmic amplifier?
lin_gain = 1e9                                             # linear amplifier
resolution = 16.0                                          # ADWin is 16 bits
clockfrequency = 40.0e6                                    # ADwin frequency Hz
clockfrequencylow=1e4                                      #ADwin frequency low priority process
refresh_rate = 10.0                                         # Hz
log_conversion = read_data_file('C:/Users/Usuario/Desktop/Programas (Por ordenar)/python programs/Ignacio/New Setup/Libs/calibrationIO.txt', 2) # logarithmic amplifier conversion table
G0 = 7.74809173e-5                                          # conductance quantum
motor_min = 1e6                                             # counts
motor_max = -5e6                                             # counts
date, runnumber = make_filename('set')

##### BOOT ADWIN #####
ADwin_boot()                                    # boot ADwin
ADwin_load_process('C:/Users/Usuario/Desktop/Programas (Por ordenar)/python programs/Ignacio/New Setup/AO1_read_MUX12.T91') # load record_IV as process 1
ADwin_load_process('C:/Users/Usuario/Desktop/Programas (Por ordenar)/python programs/Ignacio/New Setup/Gt_MUX12.T92') # load record_G(t) as process 2
ADwin_load_process('C:/Users/Usuario/Desktop/Programas (Por ordenar)/python programs/Ignacio/New Setup/Gt_MUX1.T93') # load record_G(t) as process 3
ADwin_load_process('C:/Users/Usuario/Desktop/Programas (Por ordenar)/python programs/Ignacio/New Setup/piezo_histogram.T94') # load piezo histogram as process 4
ADwin_load_process('C:/Users/Usuario/Desktop/Programas (Por ordenar)/python programs/Ignacio/New Setup/AO2.T95') # load piezo histogram as process 5
ADwin_load_process('C:/Users/Usuario/Desktop/Programas (Por ordenar)/python programs/Ignacio/New Setup/MovepiezolowP.T98')
#ADwin_load_process('C:/Users/localadmin/Google Drive/Measurements/Ignacio/New Setup/logampcali.T96')# load log amplifier calibration as process 6

##### INITIALIZE FAULHABER #####
Faulhaber_command('en')             # initialize motor
Faulhaber_command('LL 5000000')        # set max postion
Faulhaber_command('LL -7000000')    # set min position
Faulhaber_command('APL 1')          # use limits (1 = on)
Faulhaber_command('SP 800')         # set max speed (rpm)
Faulhaber_command('AC 40')          # set max acceleration (rpm/s)
Faulhaber_command('di')             # disable motor

print "Boot successful"
