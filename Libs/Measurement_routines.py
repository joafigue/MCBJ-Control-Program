##### GENERAL #######

def ADwin_record_IV(Voltage, process_delay, loops_waiting, points_av, log, lin_gain, log_conversion):
    # record I(V) using ADwin

    ## INITIALIZE ##
    V_bin, Voltage = convert_V_to_bin(Voltage,output_range,resolution)
    NumBias = len(V_bin)
    ADwin_set_data_long(1,convert_to_list(V_bin))                 # send arrays of the voltages
    ADwin_set_data_float(10,log_conversion)                 # send arrays of the voltages
    ADwin_set_processdelay(1,int(process_delay)) # set process delay
    ADwin_set_Par(55,int(points_av))             # set points to average
    ADwin_set_Par(56,int(loops_waiting))         # set settling time
    ADwin_set_Par(57,int(len(Voltage)))          # array length
    ADwin_set_Par(59, int(1))                    # process is still running

    ## RUN PROCESS ##
    ADwin_start_process(1)
    check = True
    while check:
        if (ADwin_get_Par(59) == 1):
            sleep(1 / refresh_rate)
            V_current = ADwin_get_Par(8)

            #print "Bias = %1.2f V " % convert_bin_to_V(V_current, output_range, resolution)
        else:
            ADwin_stop_process(1)
            check = False

    ## GET DATA ##
    Current1 = ADwin_get_data_float(4,NumBias)     # get averaged MUX1 current values
    Current2 = ADwin_get_data_float(5,NumBias)     # get averaged MUX1 current values
    bin1 = ADwin_get_data_long(2,NumBias)     # get averaged MUX1 bin values
    bin2 = ADwin_get_data_long(3,NumBias)     # get averaged MUX1 bin values

    if log != 1:
        Current1 = convert_bin_to_V(bin1, input_range, resolution) / lin_gain
        Current2 = convert_bin_to_V(bin2, input_range, resolution) / lin_gain


    return array(Current1), array(Current2)


def ADwin_record_Gt(start_V, set_V, end_V, Gt_time, process_delay, loops_waiting, points_av, log, lin_gain, log_conversion):
    # record G(t) using ADwin

    ## Intialize
    start_V_bin, start_V = convert_V_to_bin(start_V,output_range,resolution)
    set_V_bin, set_V = convert_V_to_bin(set_V,output_range,resolution)
    end_V_bin, end_V = convert_V_to_bin(end_V,output_range,resolution)

    total_points =  int(scanrate / points_av * Gt_time)             # get Gt total number of points

    ADwin_set_processdelay(3,int(process_delay))     # set process delay
    ADwin_set_data_float(10,log_conversion) # set log conversion table
    ADwin_set_Par(7,int(start_V_bin))                # set start voltage
    ADwin_set_Par(8,int(set_V_bin))                  # set set voltage
    ADwin_set_Par(9,int(end_V_bin))                  # set set voltage
    ADwin_set_Par(10,int(total_points)+1)              # set total run time
    ADwin_set_Par(55,int(points_av))                 # set points to average
    ADwin_set_Par(56,int(loops_waiting))             # set settling time
    ADwin_set_Par(59,1)                              # 1 =  process is running; 2 = process is finished

    ## RUN PROCESS ##
    ADwin_start_process(3)
    sleep(0.01)

    check = True
    while check:
        if (ADwin_get_Par(59) == 1):
            sleep(1 / refresh_rate)
            t = int(ADwin_get_Par(11))
            Current1 = ADwin_get_FPar(14)
            bin1 = int(ADwin_get_Par(12))

            #print "Time = %2.2f s %1.2e" % (t / (scanrate / points_av), Current1/set_V)
        else:
            ADwin_stop_process(3)
            check = False

    ## GET DATA ##
    t = int(ADwin_get_Par(11))-1
    Current1 = ADwin_get_data_float(4,t)     # get averaged MUX1 current values
    bin1 = ADwin_get_data_long(2,t)     # get averaged MUX1 bin values

    if log != 1:
        Current1 = convert_bin_to_V(bin1, input_range, resolution) / lin_gain

    Time = range(0,t)

    return Time, Current1/set_V

def ADwin_apply_gate(start_Vg, set_Vg, end_Vg, process_delay_gate, loops_waiting_gate):
    # apply gate voltage on AO2 of ADwin

    ## Intialize
    start_Vg_bin, start_Vg = convert_V_to_bin(start_Vg,output_range,resolution)
    set_Vg_bin, set_Vg = convert_V_to_bin(set_Vg,output_range,resolution)
    end_Vg_bin, end_Vg = convert_V_to_bin(end_Vg,output_range,resolution)

    ADwin_set_processdelay(5,int(process_delay_gate))  # set process delay
    ADwin_set_Par(31,int(start_Vg_bin))                # set gate start voltage
    ADwin_set_Par(32,int(set_Vg_bin))                  # set gate voltage
    ADwin_set_Par(33,int(end_Vg_bin))                  # set gate end voltage
    ADwin_set_Par(34,int(loops_waiting_gate))          # set gate settling time
    ADwin_set_Par(38,int(0))                           # set total run time
    ADwin_set_Par(39,1)                                # 1 =  process is running; 2 = process is finished

    ## RUN PROCESS ##
    ADwin_start_process(5)

    return
