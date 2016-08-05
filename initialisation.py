from pylab import *
for i in range(0,100):
    close(i)
#### CLEAR ALL #####
import os
os.chdir('C:/Users/Usuario/Desktop/Programas (Por ordenar)/python programs/Ignacio/New Setup/')
#os.chdir('C:/Users/localadmin/Google Drive/Measurements/Mickael')
os.system('cls')

#### INITIALIZE MEASUREMENTS #####
motor = True
execfile('Libs/Boot.py')
closefigs()

##### MEASUREMENT SETTINGS #####
points_av = 50.0          #
settling_time = 10.0        # ms
scanrate = 100000.0         # Hz
integration_time= 0.0       # ms
V_per_V = 1.0           # V/V
save_dir = 'E:/Measurements/Molecula X/oro/'

##### G(t) SETTTINGS #####
start_V = 0.0            # V
set_V = 0.1  # V  (Se puede cambiar hasta 0.3)
end_V = 0.0              # V
Gt_time= 5000.0             # s (Tiempo de duracion)

##### Inistialisation settings #####
set_G =1.0     # G0    (chico para romper, grande para juntar y medir)
tolerance = 0.1           # %
init_speed = 2.0       # um/s
stop_on_target =False
move_motor =True #True # False
Save = False

##### timing settings
loops_av, process_delay, loops_waiting = get_delays(scanrate,integration_time,settling_time,clockfrequency)      # get_delays

#########################
##### RUN INITIALISATION #####
#########################

## INITIALIZE ##
start_V_bin, start_V = convert_V_to_bin(start_V / V_per_V ,output_range,resolution)
set_V_bin, set_V = convert_V_to_bin(set_V / V_per_V ,output_range,resolution)
end_V_bin, end_V = convert_V_to_bin(end_V / V_per_V ,output_range,resolution)
start_V = start_V * V_per_V
set_V = set_V * V_per_V
end_V = end_V * V_per_V

tmp = array(log10(log_conversion[-32769:-1]))
set_I = set_G * set_V * G0
set_G_bin = abs(tmp - log10(set_I)).argmin() + 32768

total_points =  int(scanrate / points_av * Gt_time)             # get Gt total number of points

ADwin_set_processdelay(2,int(process_delay))     # set process delay
ADwin_set_data_float(10,log_conversion) # set log conversion table
ADwin_set_Par(7,int(start_V_bin))                # set start voltage
ADwin_set_Par(8,int(set_V_bin))                  # set set voltage
ADwin_set_Par(9,int(end_V_bin))                  # set set voltage
ADwin_set_Par(10,int(total_points))              # set total run time
ADwin_set_Par(55,int(points_av))                 # set points to average
ADwin_set_Par(56,int(loops_waiting))             # set settling time
ADwin_set_Par(59,1)                              # 1 =  process is running; 2 = process is finished

## RUN PROCESS ##
ADwin_start_process(2)
sleep(0.01)

# Set up the figure
rcParams['figure.figsize'] = [12, 10]
fig = figure()
ax = subplot(111)
line, = ax.plot([], [], lw=2)
ax.set_xlim([0, 1000])
ax.set_ylim([1e-8, 10000])
ax.set_yscale('log')
ax.set_ylabel('Conductance (G0)')
ax.set_xlabel('Time (s)')
fig.set_facecolor('white')
font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 22}
matplotlib.rc('font', **font)
#ax.autoscale(enable=True, axis='both', tight=None)

Gt_1 = []
Time = []
breaking = True
stopped = True
text = 'stopped'
Run = True

while Run:
    ## get data ##
    sleep(0.01)
    t = ADwin_get_Par(11) / scanrate * points_av
    Current1 = ADwin_get_FPar(14)
    bin1 = int(ADwin_get_FPar(12))

    if log != 1:
        Current1 = convert_bin_to_V(bin1, input_range, resolution) / lin_gain

    Gt_1.append(Current1 / set_V / G0)
    Time.append(t)
    if motor:
        axispos = int(Faulhaber_command('pos'))
    else:
        axispos = 0
        text = 'Off'
    line.set_data(Time, Gt_1)
    ax.set_xlim([Time[0], Time[-1]*1.2])
    pause(0.001)

    os.system('cls')
    print "Time (s)    G (G0)    Motor    Status"
    print("%3.2fs    %1.2e  %d  %s"%(t, Current1 / set_V / G0, axispos, text))

    ## stop if stop_on_target is on
    if (abs((bin1 - set_G_bin) / float(set_G_bin) ) <= tolerance/100) & move_motor:
        text =  'In range'
        Faulhaber_command('v 0')
        stopped = True
        if stop_on_target:
            ADwin_stop_process(2)
            Run = False

    if (abs((bin1 - set_G_bin) / float(set_G_bin) ) > tolerance/100) & (bin1 < set_G_bin) & move_motor:
        #Faulhaber_command('v 0')
        text = 'Making'
        if (breaking == True) | (stopped == True):
            Faulhaber_continuous(init_speed, False)
            breaking = False
            stopped = False

    if (abs((bin1 - set_G_bin) / float(set_G_bin) ) > tolerance/100) & (bin1 > set_G_bin) & move_motor:
        #Faulhaber_command('v 0')
        text = 'Breaking'
        if (breaking == False) | (stopped == True):
            Faulhaber_continuous(init_speed, True)
            breaking = True
            stopped = False

    if (t >= Gt_time):
        if log == False:
            bin1 = ADwin_get_data_float(2, int(round(Gt_time * (scanrate/points_av))))     # get averaged MUX1 bin values
            Conductance = convert_bin_to_V(bin1, input_range, resolution) / lin_gain
            Conductance = Conductance / set_V / G0
            Time = linspace(0, Gt_time,len(Conductance))
        else:
            Conductance = ADwin_get_data_float(4, int(round(Gt_time * (scanrate/points_av)))) / set_V / G0    # get averaged MUX1 bin values
            Time = linspace(0, Gt_time,len(Conductance))

        if Save:
            filename = save_dir + 'Conductance' + date + '_' + runnumber + '.dat'
            file = open(filename, "w")
            make_general_header(file)
            save_data(file, Time, Conductance)
            file.close()

        ADwin_stop_process(3)
        Run = False
