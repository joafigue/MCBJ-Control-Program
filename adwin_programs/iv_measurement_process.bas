'<ADbasic Header, Headerversion 001.001>
' Process_Number                 = 1
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

' This program provides a continuous measurement of the current at the sample
' driven by the set voltage. In order to interface with the computer several
' ADwin static variables are used

'*******
' Inputs: Set by external program
'*******
' ---- Juncture Voltage Parameters ----
' PAR_1 -> Initial juncture voltage (off)
' PAR_2 -> Juncture voltage for measurement
' PAR_3 -> Juncture voltage at end (off)
' ---- Current Measurement ----
' PAR_7 -> Number of loops to wait after reaching desired juncture
'          voltage before starting measuremnts
' PAR_8 -> Number of data point to average for current measurement
' ---- Measurement Modifiers ----
' PAR_10 -> Maximum number of data points to gather
' PAR_11 -> Set to 1 to finish the run early
' ---- Logaritmic amplifier ----
' DATA_10 -> The calibration data for the logaritmic amplifier

'******
' Outputs
'******
' ---- Current Measurements ----
' FPAR_1 -> Current measured in channel 1
' FPAR_2 -> Current measured in channel 1 through Amplifier
' FPAR_3 -> Current measured in channel 2
' FPAR_4 -> Current measured in channel 2 through Amplifier
' ---- Measurement end ----
' PAR_12 -> State parameter, to check which case we are
' PAR_13 -> Set to 1 when the measurement process is finished


'******
' Aux variables
'******
' waitcounter -> Used to wait for stabilization before measuring (JV)
' avgcounter -> Used to select how many points will be averaged
' datacounter -> Used to count how many data points will be stored in total
' juncture_voltage -> Corrent juncture voultage at DAC
' current_acc -> Variables to store the accumulated value for averaging
' current_ampl_acc -> Same as before, but measured through log-amplifier

DIM waitcounter, avgcounter, datacounter  as long
DIM juncture_voltage as long
DIM current1_acc, current2_acc as long
DIM current1_amp_acc, current2_amp_acc as float
' Set DATA_10 as amplifier array
DIM DATA_10[65536] as float

INIT:
  PAR_12 = 0
  PAR_13 = 0
  waitcounter = 0
  avgcounter = 0
  datacounter = 0
  current1_acc = 0
  current2_acc = 0
  current1_amp_acc = 0
  current2_amp_acc = 0
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

    CASE 1 ' Wait untill stabilization
      IF(waitcounter = PAR_7) THEN
        PAR_12 = 2
      ELSE
        waitcounter = waitcounter + 1
      ENDIF

    CASE 2 ' Measure
      START_CONV(00011b)
      WAIT_EOC(00011b)
      current1_acc = current1_acc + READADC(1)
      current2_acc = current2_acc + READADC(2)
      current1_amp_acc = current1_amp_acc + DATA_10[READADC(1)+1]
      current2_amp_acc = current2_amp_acc + DATA_10[READADC(2)+1]
      avgcounter = avgcounter + 1
      
      IF(avgcounter = PAR_8) THEN
        FPAR_1 = current1_acc / PAR_8
        FPAR_3 = current2_acc / PAR_8
        FPAR_2 = current1_amp_acc / PAR_8
        FPAR_4 = current2_amp_acc / PAR_8
        datacounter = datacounter + 1
        avgcounter = 0
        current1_acc = 0
        current2_acc = 0
        current1_amp_acc = 0
        current2_amp_acc = 0
      ENDIF
      
      IF (datacounter = PAR_10) THEN PAR_12 = 3
      IF (PAR_11 = 1) THEN PAR_12 =3

    CASE 3 'ramp down to end voltage
      IF(juncture_voltage < PAR_3 ) THEN INC(juncture_voltage)
      IF(juncture_voltage > PAR_3) THEN DEC(juncture_voltage)
      DAC(1, juncture_voltage)
      IF  (juncture_voltage = PAR_3) THEN PAR_13 = 1 ' check for end measurement

  ENDSELECT
