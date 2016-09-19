# [[file:../Measure_samples.org::*Faulhaber%20Driver][Faulhaber\ Driver:1]]
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
# Faulhaber\ Driver:1 ends here

# [[file:../Measure_samples.org::src-faulhaber-constants][src-faulhaber-constants]]
#################################################################
## @author  Joaquin Figueroa
#  @brief   Constants used for the faulhaber interface
#
#  @details These are the constants used by the faulhaber
#           interface.
#################################################################
class fh_const:
    port = "COM3" #
    baud_rate = 9600 #
    pitch = 150 #
    gearbox = 246 #
    max_pos =  5000000#
    min_pos = -7000000#
    max_speed = 800#in RPM
    max_accel = 40#in RPM/s
# src-faulhaber-constants ends here

# [[file:../Measure_samples.org::faulhaber-class-def][faulhaber-class-def]]
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
        self.motor_ctrl = visa.SerialInstrument(fh_const.port)
        self.motor_ctrl.baud_rate = fh_const.baud_rate
    ###  Beware the interface may not be completely correct
        self._enable_motor()
        self._set_pos_range()
        self._set_respect_user_limits()
        self._set_max_speed()
        self._set_max_acceleration()
        self._disable_motor()
    #################################################################
    ## @brief   Enables the motor
    #################################################################
    def _enable_motor(self):
        self.motor_ctrl.write("en")
    #################################################################
    ## @brief   Disables the motor
    #################################################################
    def _disable_motor(self):
        self.motor_ctrl.write("di")
    #################################################################
    ## @brief   Ensures that the motor honor the user defined limits
    #################################################################
    def _set_respect_user_limits(self):
        self.motor_ctrl.write("APL 1")
    #################################################################
    ## @brief   Set the maximum and minimum position for the motor axis
    #################################################################
    def _set_pos_range(self):
        max_pos_str = "LL %d" % fh_const.max_pos
        min_pos_str = "LL %d" % fh_const.min_pos
        self.motor_ctrl.write(max_pos_str)
        self.motor_ctrl.write(min_pos_str)
    #################################################################
    ## @brief   Sets the maximum speed for the motor
    #################################################################
    def _set_max_speed(self):
        max_speed_str = "SP %d" %fh_const.max_speed
        self.motor_ctrl.write(max_speed_str)
    #################################################################
    ## @brief   Sets the maximum acceleration for the motor
    #################################################################
    def _set_max_acceleration(self):
        max_accel_str = "SP %d" %fh_const.max_accel
        self.motor_ctrl.write(max_accel_str)
    #################################################################
    ## @brief   Sets the target speed of the motor
    #################################################################
    def _set_target_speed(self,speed):
        target_speed_str = "v %d" %speed
        self.motor_ctrl.write(target_speed_str)
    #################################################################
    ## @brief   Returns the current axis position
    #################################################################
    def _query_current_axis_position(self):
        pos = self.motor_ctrl.query("pos")
        try:
            int(pos)
        except:
            self._set_target_speed(0)
            sleep(0.1)
            self._disable_motor()
            print("Error, Returned position was not a valid int")
            print(pos)
            raise
# faulhaber-class-def ends here
