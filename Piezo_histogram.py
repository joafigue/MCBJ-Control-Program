#### CLEAR ALL #####
import os
os.chdir('C:/Users/Usuario/Desktop/Programas (Por ordenar)/python programs/Ignacio/New Setup/')
os.system('cls')
from numpy import *
from pylab import *

##### INITIALIZE MEASUREMENTS #####
execfile('C:/Users/Usuario/Desktop/Programas (Por ordenar)/python programs/Ignacio/New Setup/Libs/Boot.py')
closefigs()

save_dir ='E:/Measurements/Fullerenos/C60 2/Molecule/'
#save_dir ='D:/Diana/curcuminoid pyridine2/molecule/'

##### MEASUREMENT SETTINGS #####
#points_av = 16.0    #
settling_time = 0.0        # ms
#scanrate = 60000.0        # Hz
#points_av = 16.0    #
#scanrate = 64000.0        # Hz
points_av =32.0    # 32 (300V/s) 96 (30V/s)
scanrate =102400.0   #102400 (300V/s)  76000 (30V/s)   # Hz
integration_time= 0.0       # ms
save = 1
Plot = 1

##### Voltage SETTTINGS #####
start_V = 0.0            # V
set_V = 0.1 # V (Bias V)

##### Histogram settings #####
piezo_start_V = 0.0         # V
high_G = 30.0              # G0
inter_G = 20.0              # G0
low_G = 10.0              # G0
piezo_speed_breaking1 = 300.0        # V/s
piezo_speed_breaking2 = 300.0        # V/s (30 to 300) Este es el que se puede cambiar
piezo_speed_making = 500.0        # V/s
#post_breaking_voltage = 230.0       #
post_breaking_voltage = 300.0       # cambia cuanto abro despues de que rompo
number_traces = 5000                   #
nGbins = 251
nDbins = 161
xmin = -0.5 # nm
xmax = 2    # nm
Gmin = 1e-7 # G0
Gmax = 10   # G0

##### timing settings
loops_av, process_delay, loops_waiting = get_delays(scanrate,integration_time,settling_time,clockfrequency)      # get_delays
piezo_wait_cycles_breaking1 = int(scanrate / ((piezo_speed_breaking1 / 100) / (2*output_range/2**resolution)))   # get wait loop for piezo
piezo_wait_cycles_breaking2 = int(scanrate / ((piezo_speed_breaking2 / 100) / (2*output_range/2**resolution)))   # get wait loop for piezo
piezo_wait_cycles_making = int(scanrate / ((piezo_speed_making / 100) / (2*output_range/2**resolution)))   # get wait loop for piezo

#########################
##### RUN INITIALISATION #####
#########################

## INITIALIZE ##
start_V_bin, start_V = convert_V_to_bin(start_V,output_range,resolution)
piezo_start_V_bin, start_V = convert_V_to_bin(piezo_start_V,output_range,resolution)
set_V_bin, set_V = convert_V_to_bin(set_V,output_range,resolution)

high_I = high_G * set_V * G0
inter_I = inter_G * set_V * G0
low_I = low_G * set_V * G0
post_breaking_points = int(post_breaking_voltage / piezo_speed_breaking2 * (scanrate / points_av))

ADwin_set_processdelay(4,int(process_delay))     # set process delay
ADwin_set_data_float(10,log_conversion)          # set log conversion table

ADwin_set_Par(1,int(piezo_start_V_bin))                # set start voltage
ADwin_set_Par(7,int(start_V_bin))                # set start voltage
ADwin_set_Par(8,int(set_V_bin))                  # set set voltage

ADwin_set_FPar(20,high_I)                  # set high I
ADwin_set_FPar(21,inter_I)                  # set intermediate I
ADwin_set_FPar(22,low_I)                  # set low I

ADwin_set_Par(23,int(piezo_wait_cycles_breaking1))                 # set points to average
ADwin_set_Par(24,int(piezo_wait_cycles_breaking2))                 # set points to average
ADwin_set_Par(25,int(piezo_wait_cycles_making))                 # set points to average
ADwin_set_Par(26,int(post_breaking_points))                 # set points to average

ADwin_set_Par(55,int(points_av))                 # set points to average
ADwin_set_Par(59,1)                              # 1 =  process is running; 2 = process is finished
ADwin_set_Par(60,0)                              # 0 =  process did not crash; 1 = process did crash

stopped = True

## initialize histogram
Gbins = power(zeros(nGbins) + 10.0, linspace(log10(Gmin), log10(Gmax), nGbins)) # create conductance array
Dbins = linspace(xmin, xmax, nDbins) # create displacement array

histo1D_breaking_sum = zeros(nGbins-1)
histo1D_making_sum = zeros(nGbins-1)
histo2D_breaking_sum = zeros(shape=(nGbins-1,nDbins-1))

## plot settings
rcParams['figure.figsize'] = [22, 10]
font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 22}
fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
ax1.set_position([0.07, 0.1, 0.25, 0.8])
ax2.set_position([0.39, 0.1, 0.25, 0.8])
ax3.set_position([0.72, 0.1, 0.25, 0.8])
fig.set_facecolor('white')
matplotlib.rc('font', **font)

#switch_backend('wxagg')

## RUN PROCESS ##
for x in range(0,number_traces):

    run = True
    while run:
        if (ADwin_get_Par(59) == 1) & stopped: # start for the first time
            ADwin_start_process(4)
            stopped = False

        if (ADwin_get_Par(59) == 2) & (stopped == False): # stop when done trace
            ADwin_stop_process(4)
            stopped = True
            ADwin_set_Par(59,1)
            run = False
            length_breaking = ADwin_get_Par(2)-1
            length_making = ADwin_get_Par(3)-1

            G_breaking = (ADwin_get_data_float(2, length_breaking)) / (set_V * G0)
            T_breaking = array(range(0, length_breaking)) / (scanrate / points_av)
            G_making = ADwin_get_data_float(4, length_making)/ (set_V * G0)
            T_making = array(range(0, length_making)) / (scanrate / points_av)

            D_breaking =  T_breaking * piezo_speed_breaking2 * 0.02 # length calibration value based on Au 1 G0 plateau
            D_making =  T_making * piezo_speed_making * 0.02

            if Plot == 1:
                # plot traces (1)
                ax1.clear()
                plt_breaking =  ax1.plot(D_breaking,G_breaking,linewidth=2)
                plt_making =  ax1.plot(D_making,G_making,linewidth=2)
                ax1.set_yscale("log")
                ax1.set_xlim(0, max(max(D_making),max(D_breaking)))
                ax1.set_ylim(Gmin, Gmax)
                ax1.set_title("Conductance trace")
                ax1.set_xlabel('Displacement (nm)')
                ax1.set_ylabel('Conductance (G0)')
                ax1.set_aspect(1)
                #ax1.xticks(power(zeros(nGbins) + 10.0, range(-8,2,4)))
                #ax1.yticks(range(-10,1,10))

                tmp=histogram(G_breaking, bins=Gbins)
                histo1D_breaking_sum = histo1D_breaking_sum + tmp[0]
                tmp=histogram(G_making, bins=Gbins)
                histo1D_making_sum = histo1D_making_sum + tmp[0]

                # plot 1D histogram (2)
                Gbins_plot = Gbins[0:-1]
                Dbins_plot = Dbins[0:-1]
                ax2.clear()
                plt_histo1D_breaking =  ax2.plot(Gbins_plot,histo1D_breaking_sum,linewidth=2)
                plt_histo1D_making =  ax2.plot(Gbins_plot,histo1D_making_sum,linewidth=2)
                ax2.set_xscale("log")
                ax2.set_ylim(0, 1.2*max(max(histo1D_making_sum),max(histo1D_making_sum)))
                ax2.set_xlim(Gbins[0], Gbins[-1])
                ax2.set_title("1D Histogram")
                ax2.set_ylabel('Counts')
                ax2.set_xlabel('Conductance (G0)')
                ax2.set_aspect(1)

                index=max(find(G_breaking>0.5))
                D_breaking = D_breaking - D_breaking[index]

                # plot 2D histogram (3)
                tmp = histogram2d(G_breaking, D_breaking, bins=(Gbins, Dbins))
                histo2D_breaking_sum = histo2D_breaking_sum + tmp[0]

                index1 = find(min(abs(log10(Gbins) - -2 ))==(abs(log10(Gbins) - -2 )))
                index2 = find(min(abs(log10(Gbins) - -6 ))==(abs(log10(Gbins) - -6 )))
                tmp = histo2D_breaking_sum[index2:index1,:]

                Cmax = 0
                for y in range(0,index1-index2):
                    Cmax = max(max(tmp[y,:]), Cmax)

                ax3.clear()
                surf = ax3.contourf(Dbins_plot, Gbins_plot, histo2D_breaking_sum, linspace(0,Cmax/2,16))
                ax3.set_yscale("log")
                ax3.set_ylim(Gbins_plot[0], Gbins_plot[-1])
                ax3.set_xlim(Dbins_plot[0], Dbins_plot[-1])
                ax3.set_title("2D Histogram")
                ax3.set_xlabel('Displacement (nm)')
                ax3.set_ylabel('Conductance (G0)')

                pause(1)

            if save == 1:
              filename = save_dir + 'scan' + date + '_' + runnumber + '_' + "%1.0f.dat" % x
              file = open(filename, "w")
              #make_general_header(file)
              make_piezo_header(file)
              save_data(file, T_breaking, G_breaking)
              save_data(file, T_making, G_making)
              file.close()


        os.system('cls')
        if (ADwin_get_Par(4) == 1):
            print 'Run number: %1.0f \nbreaking 1'% x

        if (ADwin_get_Par(4) == 2):
            print 'Run number: %1.0f \nbreaking 2'% x

        if (ADwin_get_Par(4) == 3):
            print 'Run number: %1.0f \npost breaking'% x

        if (ADwin_get_Par(4) == 4):
            print 'Run number: %1.0f \nmaking'% x
