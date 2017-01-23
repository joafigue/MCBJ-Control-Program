# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::*Faulhaber%20Driver][Faulhaber Driver:1]]
#################################################################
## @file    Faulhaber_driver.py
#  @author  Joaquin Figueroa
#  @date    Sun Sep 18, 2016
#  @brief   Provides the interfaces for the Faulhaber motor
#
#  @details This file provides only the faulhaber interface,
#           which defines high and low level functionalities.
#           The user should use the high level functionality
#           if possible.
#           Also this file provides with some extra utilities
#           that are not necesary inside the same faulhaber
#           class.
#################################################################
import visa
# Faulhaber Driver:1 ends here

# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::src-faulhaber-constants][src-faulhaber-constants]]
#################################################################
## @author  Joaquin Figueroa
#  @brief   Constants used for the faulhaber interface
#
#  @details These are the constants used by the faulhaber
#           interface.
#################################################################
class FH_CONST:
    port = "COM3" #
    baud_rate = 9600 #
    pitch = 150 #
    gearbox = 246 #
    max_pos = 5000000#
    min_pos = -7000000#
    max_speed = 800#in RPM
    max_accel = 40#in RPM/s
# src-faulhaber-constants ends here

# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::*Conversion%20functions][Conversion functions:1]]
#################################################################
## @brief   Converts motor speed from um/s to rpm
#################################################################
def faulhaber_convert_ums_to_rpm(ums):
    rpm = 60 * gearbox * (ums / pitch)
    return rpm

#################################################################
## @brief   Converts motor speed from rpm to um/s
#################################################################
def faulhaber_convert_rpm_to_ums(rpm):
    ums = (rpm * pitch)/( 60 * gearbox)
    return ums
# Conversion functions:1 ends here

# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::*Faulhaber%20State][Faulhaber State:1]]
class faulhaber_state():
    def __init__(self, start_pos, start_speed):
        self.start_pos = start_pos
        self.current_speed = start_speed
        self.previous_pos = [start_pos, start_pos, start_pos]
    def update_position(self, new_pos):
        self.previous_pos.append(new_pos)
        self.previous_pos.pop(0)
    # Depends on numpy abs to work on array
    def is_motor_stopped(self):
        a = self.previous_pos
        delta = sum(abs([a.[2] - a.[1], a.[1]-a.[0]]))
        return delta==0
    def update_current_speed(self, new_speed):
        self.current_speed = new_speed
# Faulhaber State:1 ends here

# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::faulhaber-class-def][faulhaber-class-def]]
#################################################################
## @author  Joaquin Figueroa
#  @brief   Faulhaber class interface
#
#  @details These are the constants used by the faulhaber
#           interface.
#################################################################
class Faulhaber_motor:
    def __init__(self): #(ref:fh-init-fn)
    ###  Beware the interface may not be completely correct
        self.motor_ctrl = visa.SerialInstrument(FH_CONST.port)
        self.motor_ctrl.baud_rate = FH_CONST.baud_rate
    ###  Beware the interface may not be completely correct
        self.enable_motor()
        self.set_pos_range()
        self.set_respect_user_limits()
        self.set_max_speed()
        self.set_max_acceleration()
        self.disable_motor()
        self.state = self.init_state()
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::faulhaber-basic-fn-interface][faulhaber-basic-fn-interface]]
    #################################################################
    ## @brief   Enables the motor
    #################################################################
    def enable_motor(self):
        self.motor_ctrl.write("en")
    # faulhaber-basic-fn-interface ends here
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::faulhaber-basic-fn-interface][faulhaber-basic-fn-interface]]
    #################################################################
    ## @brief   Disables the motor
    #################################################################
    def disable_motor(self):
        self.motor_ctrl.write("di")
    # faulhaber-basic-fn-interface ends here
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::faulhaber-basic-fn-interface][faulhaber-basic-fn-interface]]
    #################################################################
    ## @brief   Ensures that the motor honor the user defined limits
    #################################################################
    def set_respect_user_limits(self):
        self.motor_ctrl.write("APL 1")
    # faulhaber-basic-fn-interface ends here
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::faulhaber-basic-fn-interface][faulhaber-basic-fn-interface]]
    #################################################################
    ## @brief   Set the maximum and minimum position for the motor axis
    #################################################################
    def set_pos_range(self):
        max_pos_str = "LL %d" % FH_CONST.max_pos
        min_pos_str = "LL %d" % FH_CONST.min_pos
        self.motor_ctrl.write(max_pos_str)
        self.motor_ctrl.write(min_pos_str)
    # faulhaber-basic-fn-interface ends here
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::faulhaber-basic-fn-interface][faulhaber-basic-fn-interface]]
    #################################################################
    ## @brief   Sets the maximum speed for the motor
    #################################################################
    def set_max_speed(self):
        max_speed_str = "SP %d" %FH_CONST.max_speed
        self.motor_ctrl.write(max_speed_str)
    # faulhaber-basic-fn-interface ends here
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::faulhaber-basic-fn-interface][faulhaber-basic-fn-interface]]
    #################################################################
    ## @brief   Sets the maximum acceleration for the motor
    #################################################################
    def set_max_acceleration(self):
        max_accel_str = "SP %d" %FH_CONST.max_accel
        self.motor_ctrl.write(max_accel_str)
    # faulhaber-basic-fn-interface ends here
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::faulhaber-basic-fn-interface][faulhaber-basic-fn-interface]]
    #################################################################
    ## @brief   Sets the target speed of the motor
    #################################################################
    def set_target_speed(self, speed):
        target_speed_str = "v %d" %speed
        self.state.update_speed(speed)
        self.motor_ctrl.write(target_speed_str)
    # faulhaber-basic-fn-interface ends here
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::faulhaber-basic-fn-interface][faulhaber-basic-fn-interface]]
    #################################################################
    ## @brief   Returns the current axis position
    #  @Note    Not to be used directly in other parts of the program
    #################################################################
    def query_current_axis_position(self):
        pos = self.motor_ctrl.query("pos")
        try:
            pos = int(pos)
            return pos
        except:
            self.set_target_speed(0)
            sleep(0.1)
            self.disable_motor()
            print("Error, Returned position was not a valid int")
            print(pos)
            raise
    
    #################################################################
    ## @brief   Returns the current axis position, updates the state
    #################################################################
    def query_position(self):
        pos = self.query_current_axis_position()
        self.state.update_position(pos)
        return pos
    # faulhaber-basic-fn-interface ends here
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::faulhaber-basic-fn-interface][faulhaber-basic-fn-interface]]
    #################################################################
    ## @brief   Initializes the motor state
    #################################################################
    def init_state(self):
        start_pos = self.query_current_axis_position()
        self.state = faulhaber_state(start_pos, 0)
    # faulhaber-basic-fn-interface ends here
# faulhaber-class-def ends here
