'<ADbasic Header, Headerversion 001.001>
' Process_Number                 = 2
' Initial_Processdelay           = 400
' Eventsource                    = Timer
' Control_long_Delays_for_Stop   = No
' Priority                       = High
' Version                        = 1
' ADbasic_Version                = 6.0.0
' Optimize                       = Yes
' Optimize_Level                 = 1
' Stacksize                      = 1000
' Info_Last_Save                 = USUARIO-PC  Usuario-pc\Usuario
'<Header End>

'*******
' Inputs: Set by external program
'*******
' ---- Juncture Voltage Parameters ----
' PAR_1 -> Initial juncture voltage (off)
' PAR_2 -> Juncture voltage for measurement
' PAR_3 -> Juncture voltage at end (off)
' ---- Piezo Voltage ----
' PAR_5 -> Initial Piezo Voltage
' ---- Current Measurement ----
' PAR_17 -> Stabilizing time for breaking
' PAR_27 -> Number of measuremnets performed during post-breaking
' PAR_18 -> Stabilizing time for making
' PAR_19 -> Number of data point to average for each measurement
' ---- Measurement Modifiers ----
' FPAR_9  -> Pre-Breaking Current -> At this point we don't skip up to complete
'            breaking to over-represent this segment(which is the target of measurement)
' FPAR_10 -> Maximum current at breaking end - Greater => not broken
' FPAR_11 -> Minimum current at making  - Smaller => not closed
' ---- Amplifier -----
' DATA_10 -> Amplifier table for calibration

'******
' Outputs
'******
' ---- Measurement end ----
' ---- Measurement end ----
' PAR_12 -> State parameter, to check which case we are
' PAR_13 -> Set to 1 when the measurement process is finished
' PAR_14 -> Set to 1 when there is a problem in the measurement
' ---- Current Measurements ----
' DATA_1 -> Array of measured currents for each data point -> breaking
' DATA_2 -> Array of set Piezo voltage for each data point -> breaking
' DATA_3 -> Array of measured currents for each data point -> making
' DATA_4 -> Array of set Piezo voltage for each data point -> making
' PAR_20 -> Final data point in  break histogram
' PAR_21 -> Final data point in  make histogram

'******
' Aux Variables
'******
' breakwait -> Used to wait for stabilization during breaking
' broken -> Used to determine if we have crossed the breaking current threshold
' break_counter -> Used to count the post breaking measurements
' makewait -> Used to wait for stabilization during making
' skip -> Used to keep track if we should skip data points or not.
' skipcounter -> Used to determine if the current datapoint should be stored
' avgcounter -> Used to count the measurements to average for a data point
' avgcurrent -> Auxiliar variable for average current
' juncture_voltage -> Current juncture_voltage at the DAC
' break_acc -> Accumulator for measurements during breaking
' make_acc -> Accumulator for measurements during making
' piezo_V -> Piezoelectric voltage
' piezo_min -> Minimum voltage to set in the piezo
' piezo_max -> Maximum voltage to set in the piezo

DIM breakwait, makewait as long
DIM broken, break_counter as long
DIM skip, skipcounter as long
DIM avgcounter  as long
DIM juncture_voltage as long
DIM break_acc, make_acc  as float
DIM piezo_V, piezo_min, piezo_max as long
DIM avgcurrent as float
' Output histogram
DIM break_hist_flag, make_hist_flag as long
DIM DATA_1[65533] as float  'Break Conductances
DIM DATA_2[65533] as float  'Break Voltages
DIM DATA_3[65533] as float  'Make Conductances
DIM DATA_4[65533] as float  'Make Voltages
' Set DATA_10 as amplifier array
DIM DATA_10[65536] as float

INIT:
  PAR_12 = 0
  PAR_13 = 0
  PAR_14 = 0
  break_hist_flag = 0
  make_hist_flag = 0
  breakwait = 0
  broken = 0
  break_counter = 0
  makewait = 0
  skip = 1
  skipcounter = 1
  avgcounter = 0
  avgcurrent = 0
  break_acc = 0
  make_acc = 0
  piezo_V = 32768               ' Start at 0 [V]
  piezo_min = 32768             ' 0  [V] at adwin output
  piezo_max = 65532             ' 10 [V] at adwin output
  PAR_20 = 1                    ' Break index
  PAR_21 = 1                    ' Make index
  ' Set juncture voltage at output and prepare measurement
  juncture_voltage = PAR_1
  DAC(1, juncture_voltage)
  set_MUX(1010000000b) 'use MUX

EVENT:

  SELECTCASE PAR_12
    CASE 0 'output desired voltage on DAC1
      ' PAR_2 -> Target juncture voltage
      IF(juncture_voltage < PAR_2) THEN INC(juncture_voltage)
      IF(juncture_voltage > PAR_2) THEN DEC(juncture_voltage)
      DAC(1, juncture_voltage)
      IF  (juncture_voltage = PAR_2) THEN PAR_12 = 1
      ' PAR_12 = 1 => we have to wait

    CASE 1 ' generate break histogram
      SELECTCASE break_hist_flag
        CASE 0 ' Move piezo to new point (ref:adw-brk-pz)
          breakwait = 0
          avgcounter = 0
          break_acc = 0
          INC(piezo_V)
          IF (piezo_V >= piezo_max) THEN
            PAR_12 = 2 ' Go to make histogram
            PAR_14 = PAR_14 + 1 ' Error in breaking
          ENDIF
          DAC(2, piezo_V)
          break_hist_flag = 1 ' Go to next stage
      
        CASE 1  ' Wait for stabilization (ref:adw-brk-wt)
          breakwait = breakwait + 1
          IF (breakwait >= PAR_17) THEN
            break_hist_flag = 2 ' Go to next stage
          ENDIF
      
        CASE 2  ' Measure data (ref:adw-brk-msr)
          START_CONV(00011b)
          WAIT_EOC(00011b)
          break_acc = break_acc + DATA_10[READADC(1)+1]
          avgcounter = avgcounter + 1
          IF (avgcounter  >= PAR_19) THEN
            break_hist_flag = 3 ' Go to next stage
          ENDIF
      
        CASE 3  ' Check for break measurement end (ref:adw-brk-end)
          avgcurrent = break_acc / PAR_19
          break_hist_flag = 4
          IF (avgcurrent <= FPAR_9) THEN
            skip = 0
          ENDIF
          IF (avgcurrent <= FPAR_10) THEN
            skip = 1
            broken = 1 ' We are in post-breaking regime
          ENDIF
          IF (skip >= 1) THEN
            skipcounter = skipcounter + 1
            IF (skipcounter < PAR_30) THEN
              break_hist_flag = 0
            ENDIF
          ENDIF
          IF (broken >= 1) THEN
            break_counter = break_counter + 1
          ENDIF
          IF (break_counter >= PAR_27) THEN
            PAR_12 = 2 ' Go to make histogram
            skipcounter = 1
          ENDIF
        CASE 4  ' Store average in array (ref:adw-brk-store)
          skipcounter = 1
          break_hist_flag = 0
          DATA_1[PAR_20] = avgcurrent
          DATA_2[PAR_20] = piezo_V
          PAR_20 = PAR_20 + 1
      ENDSELECT

    CASE 2 ' generate make histogram
      SELECTCASE make_hist_flag
        CASE 0 ' Move piezo to new point (ref:adw-mk-pz)
          makewait = 0
          avgcounter = 0
          make_acc = 0
          DEC(piezo_V)
          IF (piezo_V <= piezo_min) THEN
            PAR_12 = 3 ' Go to end process
            IF (avgcurrent <= FPAR_11) THEN
              PAR_14 = PAR_14 + 2 ' Go to end process
            ENDIF
      
          ENDIF
          DAC(2, piezo_V)
          make_hist_flag = 1 ' Go to next stage
      
        CASE 1  ' Wait for stabilization (ref:adw-mk-wt)
          makewait = makewait + 1
          IF (makewait >= PAR_18) THEN
            make_hist_flag = 2 ' Go to next stage
          ENDIF
      
        CASE 2  ' Measure data (ref:adw-mk-msr)
          START_CONV(00011b)
          WAIT_EOC(00011b)
          make_acc = make_acc + DATA_10[READADC(1)+1]
          avgcounter = avgcounter + 1
          IF (avgcounter  >= PAR_19) THEN
            make_hist_flag = 3 ' Go to next stage
          ENDIF
      
        CASE 3  ' Check for make measurement end (ref:adw-brk-end)
          avgcurrent = make_acc / PAR_19
          skipcounter = skipcounter + 1
          IF (skipcounter <= PAR_30) THEN
            make_hist_flag = 0
          ELSE
            skipcounter = 1
            make_hist_flag = 4
          ENDIF
      
        CASE 4  ' Store average in array  (ref:adw-mk-store)
          DATA_3[PAR_21] = avgcurrent
          DATA_4[PAR_21] = piezo_V
          PAR_21 = PAR_21 + 1
          make_hist_flag = 0
      ENDSELECT

    CASE 3 'ramp down to end voltage
      IF(juncture_voltage < PAR_3 ) THEN INC(juncture_voltage)
      IF(juncture_voltage > PAR_3) THEN DEC(juncture_voltage)
      DAC(1, juncture_voltage)
      IF  (juncture_voltage = PAR_3) THEN PAR_13 = 1 ' check for end measurement

  ENDSELECT
