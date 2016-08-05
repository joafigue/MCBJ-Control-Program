#### CLEAR ALL #####

import os
os.chdir('C:/Users/localadmin/Google Drive/Measurements/nandini')
os.system('cls')

##### INITIALIZE MEASUREMENTS #####
execfile('C:/Users/localadmin/Google Drive/Measurements/nandini/Libs/Boot.py')
closefigs()

save_dir ='C:/Users/localadmin/Google Drive/Measurements/nandini/Libs/'
##### MEASUREMENT SETTINGS #####
points_av = 20000.0          # 
settling_time = 50.0        # ms
scanrate = 90000.0         # Hz 
integration_time= 1.0       # ms

##### G(t) SETTTINGS #####
start_V = -2.5            # V
set_V = -2.5              # V
end_V = 2.5              # V
ref_resist= 1.0009e3           #ohms
#Gt_time= 6000.0             # s
save = 1                #save==1; not save==0
##### timing settings
loops_av, process_delay, loops_waiting = get_delays(scanrate,integration_time,settling_time,clockfrequency)      # get_delays

#########################
##### RUN INITIALISATION #####
#########################


## INITIALIZE ##
start_V_bin, start_V = convert_V_to_bin(start_V,output_range,resolution)
set_V_bin, set_V = convert_V_to_bin(set_V,output_range,resolution)
end_V_bin, end_V = convert_V_to_bin(end_V,output_range,resolution)
V_bin_array=range(start_V_bin,end_V_bin)
V_array=convert_bin_to_V(V_bin_array,output_range,resolution)

##set_I = set_G * set_V * G0
##set_G_bin = abs(tmp - log10(set_I)).argmin() + 32768

#total_points =  int(scanrate / points_av * Gt_time)             # get Gt total number of points  
#### SET THE ADWIN PARAMITERS ACORDINF TO YOUR CHOISE IN ADbasic  

ADwin_set_processdelay(3,int(process_delay))     # set process delay
ADwin_set_data_long(1,convert_to_list(V_bin_array))               # set the Voltages to apply
ADwin_set_data_float(10,log_conversion)                 # send arrays of the voltages
ADwin_set_data_long(2, convert_to_list(32678*ones(len(V_bin_array),dtype=int)))
ADwin_set_Par(7,int(start_V_bin))                # set start voltage
ADwin_set_Par(8,int(set_V_bin))                  # set set voltage
ADwin_set_Par(9,int(end_V_bin))                  # set set voltage
ADwin_set_Par(57,len(V_bin_array))              # length of the voltage array
ADwin_set_Par(55,int(points_av))                 # set points to average
ADwin_set_Par(56,int(loops_waiting))             # set settling time
ADwin_set_Par(59,1)                              # 1 =  process is running; 2 = process is finished

## RUN PROCESS ##
ADwin_start_process(1)    


run = True 
while run:
     if (ADwin_get_Par(59) == 2):
         #ADwin_stop_process(6)
         #ADwin_set_Par(59,1)
         run = False
         #NumBias = len(V_bin_array)
         #log_amplifier_bin = ADwin_get_data_long(2, NumBias)
         ADwin_stop_process(1)
         NumBias = len(V_bin_array)
         log_amplifier_bin = ADwin_get_data_float(2, NumBias)
         print "I'm done"
     else:
         bin_current=ADwin_get_Par(70)
         V_current = ADwin_get_Par(8)
         print "I'm working Bias = %1.2f V measuring bin %1.2f" % (convert_bin_to_V(V_current, output_range, resolution), bin_current)



if save == 1:
    filename = save_dir + 'logamp' + date + '_' + runnumber + ".txt" 
    file = open(filename, "w")
    save_data_intx(file, log_amplifier_bin, V_array/ref_resist)
    file.close()