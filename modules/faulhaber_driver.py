# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::*Faulhaber%20Driver][Faulhaber Driver:1]]
#################################################################
## @file    faulhaber_driver.py
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
import pylab as pl
import parameters as param
# Faulhaber Driver:1 ends here

# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::*Conversion%20functions][Conversion functions:1]]
#################################################################
## @brief   Converts motor speed from um/s to rpm
#################################################################
def faulhaber_convert_ums_to_rpm(ums):
    rpm = 60 * param.FH_CONST.GEARBOX * (float(ums) / param.FH_CONST.PITCH)
    return rpm

#################################################################
## @brief   Converts motor speed from rpm to um/s
#################################################################
def faulhaber_convert_rpm_to_ums(rpm):
    ums = (rpm * param.FH_CONST.PITCH)/( 60 * param.FH_CONST.GEARBOX)
    return ums
# Conversion functions:1 ends here

# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::*Faulhaber%20State][Faulhaber State:1]]
class faulhaber_state(object):
    def __init__(self, start_pos, start_speed):
        self.start_pos = start_pos
        self.current_speed = start_speed
        self.previous_pos = [start_pos]*4
    def update_position(self, new_pos):
        self.previous_pos.append(new_pos)
        self.previous_pos.pop(0)
    # Depends on numpy abs to work on array
    def is_motor_stopped(self):
        a = self.previous_pos
        delta = 0
        for idx in range(len(a) - 1):
            delta = delta + abs(a[idx+1] - a[idx])
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
class faulhaber_motor(object):
    def __init__(self): #(ref:fh-init-fn)
    ###  Beware the interface may not be completely correct
        self._reset_controller()
        self._init_state()
        self.init_motor()
    def init_motor(self):
        ###  Beware the interface may not be completely correct
        self.enable_motor()
        self._set_pos_range()
        self._set_respect_user_limits()
        self._set_max_speed_rpm()
        self._set_max_acceleration()
        self.disable_motor()
    
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::faulhaber-basic-fn-interface][faulhaber-basic-fn-interface]]
    #################################################################
    ## @brief   Reset controles
    #################################################################
    def _reset_controller(self): #(ref:fh-internal-fn-enable)
        self.motor_ctrl = visa.SerialInstrument(param.FH_CONST.PORT)
        self.motor_ctrl.baud_rate = param.FH_CONST.BAUD_RATE
    
    #################################################################
    ## @brief   Ensures that the motor honor the user defined limits
    #################################################################
    def _set_respect_user_limits(self):#(ref:fh-internal-fn-user-lim)
        self.motor_ctrl.ask("APL 1")
    
    #################################################################
    ## @brief   Set the maximum and minimum position for the motor axis
    #################################################################
    def _set_pos_range(self):#(ref:fh-internal-fn-pos-range)
        max_pos_str = "LL %d" % param.FH_CONST.MAX_POS
        min_pos_str = "LL %d" % param.FH_CONST.MIN_POS
        self.motor_ctrl.ask(max_pos_str)
        self.motor_ctrl.ask(min_pos_str)
    #################################################################
    ## @brief   Sets the maximum speed for the motor
    #################################################################
    def _set_max_speed_rpm(self):#(ref:fh-internal-fn-max-speed-rpm)
        max_speed_str = "SP %d" %param.FH_CONST.MAX_SPEED
        self.motor_ctrl.ask(max_speed_str)
    
    #################################################################
    ## @brief   Sets the maximum acceleration for the motor
    #################################################################
    def _set_max_acceleration(self):#(ref:fh-internal-fn-max-accel)
        max_accel_str = "SP %d" %param.FH_CONST.MAX_ACCEL
        self.motor_ctrl.ask(max_accel_str)
    
    #################################################################
    ## @brief   Sets the target speed of the motor in rpm
    #################################################################
    def _set_target_speed_rpm(self, speed):#(ref:fh-internal-fn-speed-rpm)
        target_speed_str = "v %1.2f" %speed
        self.state.update_current_speed(speed)
        self.motor_ctrl.ask(target_speed_str)
    
    #################################################################
    ## @brief   Returns the current axis position
    #  @Note    Not to be used directly in other parts of the program
    #################################################################
    def _query_current_axis_position(self, count=0):#(ref:fh-internal-fn-axis-pos)
        pos = self.motor_ctrl.ask("pos")
        try:
            pos = int(pos)
        except:
            if count < 2:
                self._reset_controller()
                pl.pause(0.02)
                return self._query_current_axis_position(count +1)
            print("Error, Returned position '{0}' was not a valid int".format(pos))
        return pos
    
    #################################################################
    ## @brief   Initializes the motor state
    #################################################################
    def _init_state(self):#(ref:fh-internal-fn-init-state)
        start_pos = self._query_current_axis_position()
        self.state = faulhaber_state(start_pos, 0)
    
    #################################################################
    ## @brief   Moves the motor for a small time in the direction set by speed
    #################################################################
    def _small_move_with_speed(self, speed):
        self.enable_motor()
        self.set_target_speed(speed)
        pl.pause(0.5)
        self.stop_motor()
        pl.pause(0.5)
        self.disable_motor()
    # faulhaber-basic-fn-interface ends here
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::faulhaber-basic-fn-interface][faulhaber-basic-fn-interface]]
    
    #################################################################
    ## @brief   Enables the motor
    #################################################################
    def enable_motor(self): #(ref:fh-basic-fn-enable)
        self.motor_ctrl.ask("en")
    
    #################################################################
    ## @brief   Disables the motor
    #################################################################
    def disable_motor(self):#(ref:fh-basic-fn-disable)
        self.motor_ctrl.ask("di")
    
    #################################################################
    ## @brief   Sets the target speed of the motor in us
    #################################################################
    def set_target_speed(self, speed_us):#(ref:fh-basic-fn-speed-us)
        speed_rpm = faulhaber_convert_ums_to_rpm(speed_us)
        self._set_target_speed_rpm(speed_rpm)
    
    #################################################################
    ## @brief   Returns the current axis position, updates the state
    #################################################################
    def get_position(self):#(ref:fh-basic-fn-real-axis-pos)
        pos = self._query_current_axis_position()
        self.state.update_position(pos)
        return pos
    
    def stop_motor(self):
        self.set_target_speed(0)
    
    def is_stopped(self, verbose=False):
        pos = self.get_position()
        if verbose : print("Motor pos = {0}".format(pos))
        return self.state.is_motor_stopped()
    
    def small_break(self, speed=-1.0):
        real_speed=-1*abs(speed)
        self._small_move_with_speed(real_speed)
    
    
    def small_make(self, speed=1.0):
        real_speed=abs(speed)
        self._small_move_with_speed(real_speed)
    
    # faulhaber-basic-fn-interface ends here
    # [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::faulhaber-advanced-fn-interface][faulhaber-advanced-fn-interface]]
    
    ## Manual Controls
    def set_motor_pos(self, new_pos):
        pos = int(new_pos)
        target_cmd = "ho {0}".format(pos)
        self.enable_motor()
        print("old position {0}".format(self.get_position()) )
        self.motor_ctrl.ask(target_cmd)
        print("new position {0}".format(self.get_position()) )
        self.disable_motor()
        return
    
    def move_to(self, target_pos, speed=2):
        # We dont have to be too precise.
        epsilon = 200
        in_range = False
        move_speed = abs(speed)
        self.enable_motor()
        while True :
            position = self.get_position()
            delta = target_pos - position
            in_range = abs(delta) < epsilon
            if in_range :
                self.stop_motor()
                break
            if delta > 0 :
                self.set_target_speed(move_speed)
            else:
                self.set_target_speed(-1*move_speed)
            print("Current Position = {0}".format(position))
        print("Final Position = {0}".format(self.get_position()))
        self.disable_motor()
    # faulhaber-advanced-fn-interface ends here
# faulhaber-class-def ends here
