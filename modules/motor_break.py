""" Module - Motor_break.py : This file has to move the motor untill  histogram can be measured

This file provides the interface necessary to use the motor with the
purpose of moving it in order the mechanically break the juncture,
and then be able to pinpoint the motor position so that the histogram
will be measured using the piezoelectric piece.
"""

__author__ = "Joaquin Figueroa"

import pylab as pl
import time
import os
import numpy as np
import adwin_driver as adw
import faulhaber_driver as fh
import configuration as conf
import parameters as param

class MB_STATE(object):
    BREAKING = 1
    RESTORING = 2
    FINE_TUNING = 3
    READY_ON_POINT = 4
    ERROR_STATUS = 5
    ERROR_NO_BREAK = 6
    ERROR_NO_MAKE = 7
    ERROR_INVALID_FINE_TUNING = 8


def build_hist_config_for_motor_break(iv_config):
    hist_dict = {}
    hist_dict['JunctureVoltage'] = iv_config.measure_jv.get_value()
    hist_dict['AveragePoints'] = 10
    hist_dict['BreakSpeed'] = 700
    hist_dict['PostBreakingVoltage'] = 200
    hist_dict['MakeSpeed'] = 700
    hist_dict['UseLogAmplifier'] = True
    return conf.histogram_config(hist_dict)


def histogram_to_data_list(break_histogram, make_histogram):
    brk_cond = break_histogram.get_conductance()
    mk_cond = make_histogram.get_conductance()
    skip = 300
    return np.concatenate((brk_cond[::skip], mk_cond[::skip]))


def motor_break_juncture_iterator(motor, iv_driver):
    motor.enable_motor()
    motor.set_target_speed(param.MB_CONST.BREAK_SPEED)
    state = MB_STATE.BREAKING
    while state == MB_STATE.BREAKING :
        pl.pause(0.05)
        conductance = iv_driver.get_conductance()
        if motor.is_stopped():
            state = MB_STATE.ERROR_NO_BREAK
        if conductance <= param.MB_CONST.BROKEN_CONDUCTANCE :
            state = MB_STATE.RESTORING
        yield conductance, state
    motor.stop_motor()
    motor.disable_motor()

def motor_restore_juncture_iterator(motor, iv_driver):
    motor.enable_motor()
    motor.set_target_speed(param.MB_CONST.MAKE_SPEED)
    state = MB_STATE.RESTORING
    while state == MB_STATE.RESTORING :
        pl.pause(0.05)
        conductance = iv_driver.get_conductance()
        if motor.is_stopped():
            state = MB_STATE.ERROR_NO_MAKE
        if conductance >= param.MB_CONST.RESTORE_CONDUCTANCE :
            state = MB_STATE.FINE_TUNING
        yield conductance, state
    motor.stop_motor()
    motor.disable_motor()


def motor_fine_tune_iterator(motor, adw_hist):
    on_point_counter = 0
    invalid_counter = 0
    state = MB_STATE.FINE_TUNING

    while state == MB_STATE.FINE_TUNING:
        break_hist, make_hist = adw_hist.measure_and_get_histogram()
        data_list = histogram_to_data_list(break_hist, make_hist)
        if adw_hist.error_in_breaking() and adw_hist.error_in_making():
            invalid_counter = invalid_counter +1
            if invalid_counter >= 3:
                on_point_counter = 0
                state = MB_STATE.ERROR_INVALID_FINE_TUNING
        elif adw_hist.error_in_breaking():
            motor.small_break()
            on_point_counter = 0
            invalid_counter = 0
        elif adw_hist.error_in_making():
            motor.small_make()
            on_point_counter = 0
            invalid_counter = 0
        else:
            invalid_counter = 0
            on_point_counter = on_point_counter +1
            if on_point_counter >= 3:
                state = MB_STATE.READY_ON_POINT
        for conductance in data_list:
            yield conductance, state



def motor_break_juncture_control_loop(motor, iv_config, hist_config=None):
    """ Control Loop """
    adw_iv = adw.adwin_iv_driver(iv_config)
    adw_iv.start_process()

    for conductance, state in motor_break_juncture_iterator(motor, adw_iv):
        yield conductance, state

    for conductance, state in motor_restore_juncture_iterator(motor, adw_iv):
        yield conductance, state

    if not hist_config :
        hist_config = build_hist_config_for_motor_break(iv_config)
    adw_hist = adw.adwin_hist_driver(hist_config)
    for conductance, state in motor_fine_tune_iterator(motor, adw_hist):
        yield conductance, state

def motor_break_get_loop_data(motor, iv_config):
    hist_config = build_hist_config_for_motor_break(iv_config)
    skip = 300                  # We only take one every 300 measurements
    piezo_data_time = hist_config.get_time_per_break_data_point() * skip
    start = time.time()
    new_time = time.time() - start
    iterator = motor_break_juncture_control_loop(motor, iv_config)
    for conductance, state in iterator:
        pos = motor.get_position()
        yield conductance, pos, state, new_time
        if state == MB_STATE.FINE_TUNING:
            new_time = new_time + piezo_data_time
        else :
            new_time = time.time() - start


def print_motor_break_data(conductance, pos, state, new_time):
    os.system('cls')
    if state == MB_STATE.BREAKING:
        print("Breaking with the Motor\n")
    if state == MB_STATE.RESTORING:
        print("Restoring with the Motor\n")
    if state == MB_STATE.FINE_TUNING:
        print("Fine Tuning  with the piezo\n")
    print("Motor pos = {0}, Conductance = {1}, Time = {2}".format(pos, conductance, new_time))

def print_motor_break_error_message(state):
    if state == MB_STATE.ERROR_STATUS:
        print("ERROR: Undefined error")
    if state == MB_STATE.ERROR_NO_BREAK:
        print("ERROR: Could not break the juncture with the motor")
    if state == MB_STATE.ERROR_NO_MAKE:
        print("ERROR: Could not restore the juncture with the motor")
    if state == MB_STATE.ERROR_INVALID_FINE_TUNING:
        print("ERROR: during fine tuning. Recommend change juncture")


def motor_break_print(motor, iv_config):
    state = MB_STATE.ERROR_STATUS
    iterator = motor_break_get_loop_data(motor, iv_config)
    for conductance, pos, state, new_time  in iterator:
        print_motor_break_data(conductance, pos, state, new_time)
        if state >= MB_STATE.ERROR_STATUS:
            print_motor_break_error_message(state)
            break
    return state

def motor_break_plot_config():
    # Set up the figure
    pl.rcParams['figure.figsize'] = [12, 10]
    fig = pl.figure()
    ax = pl.subplot(111)
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
    pl.matplotlib.rc('font', **font)
    #ax.autoscale(enable=True, axis='both', tight=None)
    return line, ax


def motor_break_print_plot(iv_config):
    motor = fh.faulhaber_motor()
    line, ax = motor_break_plot_config()

    Gt_1 = []
    Time = []

    # Set control looop which at each iteration will "spit" the state of the motro break algorithm
    state = MB_STATE.ERROR_STATUS
    motor_control_loop = motor_break_get_loop_data(motor, iv_config)
    for conductance, pos, state, new_time  in motor_control_loop:
        print_motor_break_data(conductance, pos, state, new_time)
        if state >= MB_STATE.ERROR_STATUS:
            print_motor_break_error_message(state)
            break
        Gt_1.append(conductance)
        Time.append(new_time)
        line.set_data(Time, Gt_1)
        ax.set_xlim([Time[0], Time[-1]*1.2])
        pl.pause(0.001)
    return state

def no_motor_continuous_measurement(motor, iv_config):
    adw_iv = adw.adwin_iv_driver(iv_config)
    adw_iv.start_process()
    state = MB_STATE.BREAKING
    start_time = time.time()
    while state == MB_STATE.BREAKING :
        pl.pause(0.02)
        conductance = adw_iv.get_conductance()
        new_time = time.time() - start_time
        pos = motor.get_position()
        yield conductance, pos, state, new_time

def no_motor_continuous_plot(iv_config):
    motor = fh.faulhaber_motor()
    line, ax = motor_break_plot_config()
    Gt_1 = []
    Time = []
    state = MB_STATE.ERROR_STATUS
    continuous_data  = no_motor_continuous_measurement(motor, iv_config)
    for conductance, pos, state, new_time  in continuous_data:
        print_motor_break_data(conductance, pos, state, new_time)
        if state >= MB_STATE.ERROR_STATUS:
            print_motor_break_error_message(state)
            break
        Gt_1.append(conductance)
        Time.append(new_time)
        line.set_data(Time, Gt_1)
        ax.set_xlim([Time[0], Time[-1]*1.2])
        pl.pause(0.001)
    return state

def stop():
    motor = fh.faulhaber_motor()
    motor.enable_motor()
    motor.stop_motor()
    motor.disable_motor()
    adw.adwin_driver(1, "")
