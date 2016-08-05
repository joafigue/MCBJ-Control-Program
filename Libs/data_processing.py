###################################
## Driver written by M.L. Perrin ##
## contact: m.l.perrin@tudelft.nl #
###################################

from math import log10
from numpy import *

##### MAKE GENERAL HEADER #####
def make_general_header(file):
    # make general header file for saving data
    file.write('ADwin output range : %1.2f V \n' % output_range )
    file.write('ADwin input range : %1.2f V \n' % input_range )
    if log == 1:
        file.write('logarithmic amplifier : %s \n' % log )
    else:
        file.write('linear amplifier gain : %1.0e \n' % lin_gain )
    
    Faulhaber_command('en')             # initialize motor
    pos=int(Faulhaber_command('pos')) # get motor position (counts)
    Faulhaber_command('di')             # disable motor
        
    file.write('axis position : %1.0f \n' % pos)
    file.write('points to average : %1.0f \n' % points_av )
    file.write('scanrate : %1.0f Hz \n' % scanrate)
    file.write('settling time : %1.2f ms \n' % settling_time )

##### MAKE IV SERIES HEADER #####
def make_IV_series_header(file):
    # make header file for saving data of IV series
    file.write('Gmin measure : %1.2e G0 \n' % Gmin )
    file.write('Gmax measure : %1.2e G0 \n' % Gmax_measure )
    file.write('Gmax motion reversal  : %1.2e G0 \n' % Gmax_reversal )
    file.write('stepsize  : %1.2e um\n' % stepsize )
    file.write('transition  : %1.2e G0\n' % transition_G )
##### MAKE PIEZO IV HEADER#####
def make_IV_piezo_header(file):
    # make header file for saving data of IV series
    file.write('Gmin measure : %1.2e G0 \n' % Gmin)
    file.write('Gmax measure : %1.2e G0 \n' % Gmax_measure )
    file.write('Gmax motion reversal  : %1.2e G0 \n' % Gmax_reversal )
    file.write('piezospeed1  : %1.2e um\n' % piezo_speed_breaking1 )
    file.write('piezospeed2  : %1.2e um\n' % piezo_speed_breaking2 )
    file.write('piezospeed making  : %1.2e um\n' % piezo_speed_making )
    file.write('piezo positiom  : %1.2e um\n' % piezo_position)
    file.write('transition  : %1.2e G0\n' % transition_G )
    
##### MAKE G(t)) HEADER #####
def make_Gt_header(file):
    # make header file for saving data of G(t) 
    file.write('start voltage : %1.2f V \n' % start_V)
    file.write('set voltage : %1.2f V \n' % set_V)
    file.write('end voltage : %1.2f V \n' % end_V)

##### PIEZO HEADER #####
def make_piezo_header(file):
    # make header file for saving data of G(t) 
    file.write('start voltage : %1.2f V \n' % start_V)
    file.write('set voltage : %1.2f V \n' % set_V)
    
    file.write('High G : %1.2f G0 \n' % high_G)
    file.write('Intermediate G : %1.2f G0 \n' % inter_G)
    file.write('Low G : %1.2f G0 \n' % low_G)

    file.write('Breaking speed 1 : %1.2f V/s \n' % piezo_speed_breaking1)
    file.write('Breaking speed 2 : %1.2f V/s \n' % piezo_speed_breaking2)
    file.write('Making speed : %1.2f V/s \n' % piezo_speed_making)
    
    file.write('Post breaking : %1.2f V/s \n' % post_breaking_voltage)

##### MAKE G(t)) HEADER #####
def make_gate_header(file):
    # make header file for saving data of G(t) 
    file.write('gate voltage : %1.2f V \n' % Vg)
    file.write('gate settling time : %1.2f ms \n' % settling_time_gate )    

##### MAKE MOTOR HISTOGRAM HEADER #####
def make_motor_histogram_header(file):
    # make header file for saving data of motor histogram
    file.write('start voltage : %1.2f V \n' % start_V)
    file.write('set voltage : %1.2f V \n' % set_V)
    file.write('motor speed : %1.2f um/s \n' % motor_speed)
    file.write('Gmin : %1.2e G0 \n' % Gmin)
    file.write('Gmax : %1.2e G0 \n' % Gmax_reversal)
    file.write('Imin : %1.2e G0 \n' % Imin)
    
##### SAVE DATA TO FILE #####
def save_data(*arg): 
    # write date to file. first argument is file id, all others are data arrays
    
    file = arg[0]    
    file.write('@ \n')
    
    for i in range(0,len(arg[1])):
        str = ""
        for j in range (1,len(arg)): 
            temp = arg[j]
            if j == 1:
                str = str +  "%5.8f\t" % (temp[i])
            else:
                str = str +  "%5.8e\t" % (temp[i])
            
        str = str + "\n"
        file.write(str)

    return None
def save_data_intx(*arg): 
    # write date to file. first argument is file id, all others are data arrays
    
    file = arg[0]    
    file.write('@ \n')
    
    for i in range(0,len(arg[1])):
        str = ""
        for j in range (1,len(arg)): 
            temp = arg[j]
            if j == 1:
                str = str +  "%i\t" % (temp[i])
            else:
                str = str +  "%5.8e\t" % (temp[i])
            
        str = str + "\n"
        file.write(str)

    return None    
    
    ##### GENERATE LOGARITHMIC VOLTAGE ARRAY #####
def make_log_V(minV, maxV, points):
    # generates logarithmically spaced voltage array ranging from minV to maxV with a specified number of points with no double bins
    base = 10 
    start = log10(minV)
    end = log10(maxV)
    check = True
    counter = 2
    counter_inc = 0
    inc = [100,10,1]
    
    while check:
        tmp = linspace(start, end, counter)
        tmp1 = power(zeros(len(tmp)) + base, tmp)
        tmp2 = flipud(tmp1)
        V = concatenate(([0],tmp1,tmp2, [0], -tmp1, -tmp2, [0]),axis=0)
        V_bin, V = convert_V_to_bin(V, output_range, resolution)
        V_bin = remove_double_bins(V_bin)
            
        if len(V_bin) >= points:
            counter = counter - inc[counter_inc]
            counter_inc = counter_inc + 1
            if counter_inc == len(inc):
                check = False
        else:
            counter = counter + inc[counter_inc]
            
        
    return convert_bin_to_V(V_bin, output_range, resolution)

def make_lin_V(maxV, bins_to_skip):
    # generates linearly spaced voltage array ranging from 0 to maxV with a specified number of points to skip
    range1 = arange(0, maxV+ (bins_to_skip * 2 * output_range / ( 2**resolution )), bins_to_skip * 2 * output_range / ( 2**resolution ))
    range2 = arange(range1[-1] + (bins_to_skip * 2 * output_range / ( 2**resolution )), -range1[-1] - (bins_to_skip * 2 * output_range / ( 2**resolution )) , -bins_to_skip * 2 * output_range / ( 2**resolution ))
    range3 = arange(-range1[-1] - (bins_to_skip * 2 * output_range / ( 2**resolution )), 0 + (bins_to_skip * 2 * output_range / ( 2**resolution )), bins_to_skip * 2 * output_range / ( 2**resolution ))    
    
    voltage = append(range1, range2)
    voltage = append(voltage, range3)    
    return voltage

