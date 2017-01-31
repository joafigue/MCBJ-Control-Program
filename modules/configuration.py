""" Module configuration - Defines the whole interface to configure the program

           This file defines the different configuration
           structures and interfaces, while also providing
           with the interface for the configuration file parsing

           The Main purpose of this file is to generate the
           necesary configurations for the different processes
           performed by the program
"""
__author___ = "Joaquin Figueroa"
import os
import yaml
import time
import adwin_driver as adwin
import parameters as param

class program_config(object):
    def __init__(self, data=None):
        iv_data = None
        hist_data = None
        display_data = None
        save_data = None
        if data:
            iv_data = data.get('IV Configuration')
            hist_data = data.get('Histogram Configuration')
            display_data = data.get('Display Configuration')
            save_data = data.get('Save Options')

        self.iv_config = iv_config(iv_data)
        self.hist_config = histogram_config(hist_data)
        self.display_config = display_config(display_data)
        self.save_config = save_options(save_data)

    def get_config(self):
        config = {}
        config['IV Configuration'] = self.iv_config.get_config()
        config['Histogram Configuration'] = self.hist_config.get_config()
        config['Display Configuration'] = self.display_config.get_config()
        config['Save Options'] = self.save_config.get_config()
        return config

    def dump_config_file(self, filename=None):
        data_dir = self.save_config.get_save_dir()
        if filename:
            new_filename = filename
        else:
            date = time.strftime("%Y%m%d_%H%M%S")
            new_filename = "Configuration_file_{0}.yaml".format(date)
        config_filename = os.path.join(data_dir, new_filename)
        yaml_dump(config_filename, self.get_config())
        return config_filename

class iv_config(object):
    def __init__(self, data=None):
        self.build_config_dflt()
        if data:
            self.update_config_with_data(data)

    def build_config_dflt(self):
        self.measure_jv = param.juncture_voltage()
        self.avg_points = param.avg_points()
        self.use_log_amp = param.use_log_amp()
        self.log_ampl = param.adwin_log_amplifier()
        self.move_motor = param.iv_move_motor()
        self.wait = param.GLOBAL_CONSTANTS.IV_settling_time
        self.start_jv = param.GLOBAL_CONSTANTS.start_jv
        self.end_jv = param.GLOBAL_CONSTANTS.end_jv
        self.max_data = param.GLOBAL_CONSTANTS.IV_max_data_points
        self.config = {}
        self.update_config()

    def update_config(self):
        self.config['JunctureVoltage'] = self.measure_jv.get_value()
        self.config['AveragePoints'] = self.avg_points.get_value()
        self.config['UseLogAmplifier'] = self.use_log_amp.get_value()
        self.config['MoveMotor'] = self.move_motor.get_value()

    def update_config_with_data(self, data):
        self.measure_jv.update_or_dflt(data.get('JunctureVoltage'))
        self.avg_points.update_or_dflt(data.get('AveragePoints'))
        self.use_log_amp.update_or_dflt(data.get('UseLogAmplifier'))
        self.move_motor.update_or_dflt(data.get('MoveMotor'))
        self.update_config()

    def get_config(self):
        self.update_config()
        return self.config

    def get_log_array(self):
        return self.log_ampl.get_calibration()
    def get_start_jv(self):
        return adwin.adwin_ADC(self.start_jv)
    def get_measure_jv(self):
        return adwin.adwin_ADC(self.measure_jv.get_value())
    def get_end_jv(self):
        return adwin.adwin_ADC(self.end_jv)
    def get_avg_points(self):
        return self.avg_points.get_value()
    def get_move_motor(self):
        return self.move_motor.get_value()


    def get_wait_cycles(self):
        return adwin.adwin_convert_ms_to_cycles(self.wait)
    def get_max_data(self):
        return self.max_data
    def get_real_jv(self):
        return adwin.adwin_DAC(self.get_measure_jv())
    def get_use_log_amp(self):
        return self.use_log_amp.get_value()

class histogram_config(object):
    def __init__(self, data=None):
        self.build_config_dflt()
        if data:
            self.update_config_with_data(data)

    def build_config_dflt(self):
        self.measure_jv = param.juncture_voltage()
        self.start_jv = param.GLOBAL_CONSTANTS.start_jv
        self.end_jv = param.GLOBAL_CONSTANTS.end_jv
        self.use_log_amp = param.use_log_amp()
        self.log_ampl = param.adwin_log_amplifier()
        self.avg_points = param.avg_points()
        self.break_speed = param.break_speed()
        self.post_breaking_v = param.post_breaking_voltage()
        self.make_speed = param.make_speed()
        self.skip = param.skip_points()
        self.G0 = param.GLOBAL_CONSTANTS.G0
        self.G_break_mid = 5 * self.G0
        self.G_break_end = 5e-5 * self.G0
        self.G_make_end = 20 * self.G0
        self.config = {}
        self.update_config()

    def update_config(self):
        self.config['JunctureVoltage'] = self.measure_jv.get_value()
        self.config['AveragePoints'] = self.avg_points.get_value()
        self.config['BreakSpeed'] = self.break_speed.get_value()
        self.config['PostBreakingVoltage'] = self.post_breaking_v.get_value()
        self.config['MakeSpeed'] = self.make_speed.get_value()
        self.config['SkipPoints'] = self.skip.get_value()
        self.config['UseLogAmplifier'] = self.use_log_amp.get_value()


    def update_config_with_data(self, data):
        self.measure_jv.update_or_dflt(data.get('JunctureVoltage'))
        self.avg_points.update_or_dflt(data.get('AveragePoints'))
        self.break_speed.update_or_dflt(data.get('BreakSpeed'))
        self.break_speed.update_or_dflt(data.get('PostBreakingVoltage'))
        self.make_speed.update_or_dflt(data.get('MakeSpeed'))
        self.skip.update_or_dflt(data.get('SkipPoints'))
        self.use_log_amp.update_or_dflt(data.get('UseLogAmplifier'))
        self.update_config()

    def get_config(self):
        self.update_config()
        return self.config

    def get_log_array(self):
        return self.log_ampl.get_calibration()
    def get_start_jv(self):
        return adwin.adwin_ADC(self.start_jv)
    def get_measure_jv(self):
        return adwin.adwin_ADC(self.measure_jv.get_value())
    def get_end_jv(self):
        return adwin.adwin_ADC(self.end_jv)
    def get_avg_points(self):
        return self.avg_points.get_value()

    def get_real_jv(self):
        return adwin.adwin_DAC(self.get_measure_jv())
    def get_use_log_amp(self):
        return self.use_log_amp.get_value()

    def get_break_wait(self):
        break_speed = self.break_speed.get_value()
        return adwin.aux_convert_vps_to_cycles(break_speed)
    def get_post_break_wait(self):
        post_voltage = self.post_breaking_v.get_value()/100
        return adwin.adwin_ADC(post_voltage) - adwin.adwin_ADC(0)

    def get_make_wait(self):
        make_speed = self.make_speed.get_value()
        return adwin.aux_convert_vps_to_cycles(make_speed)

    def get_skip_points(self):
        return self.skip.get_value()

    def get_I_break_mid(self):
        return  self.G_break_mid * self.get_real_jv()

    def get_I_break_end(self):
        return  self.G_break_end * self.get_real_jv()
    def get_I_make_end(self):
        return  self.G_make_end * self.get_real_jv()

    def get_time_per_break_data_point(self):
        logic_cycles = 5        # 5 logic steps in breaking
        break_wait = self.get_break_wait()
        avg_points = self.get_avg_points()
        skip_data = self.skip.get_value()
        total_cycles = (logic_cycles + break_wait + avg_points)*skip_data
        cycle_time = param.ADW_GCONST.HIGH_PERIOD * param.ADW_GCONST.PROCESS_DELAY
        time_per_data_point = cycle_time * total_cycles
        return time_per_data_point

    def get_time_per_make_data_point(self):
        logic_cycles = 5        # 5 logic steps in breaking
        break_wait = self.get_make_wait()
        avg_points = self.get_avg_points()
        skip_data = self.skip.get_value()
        total_cycles = (logic_cycles + break_wait + avg_points)*skip_data
        cycle_time = param.ADW_GCONST.HIGH_PERIOD * param.ADW_GCONST.PROCESS_DELAY
        time_per_data_point = cycle_time * total_cycles
        return time_per_data_point

class display_config(object):
    def __init__(self, data=None):
        self.build_config_dflt()
        if data:
            self.update_config_with_data(data)

    def build_config_dflt(self):
        self.xmin = param.display_xmin()
        self.xmax = param.display_xmax()
        self.Gmin = param.display_Gmin()
        self.Gmax = param.display_Gmax()
        self.nGbins = param.display_nGbins()
        self.nXbins = param.display_nXbins()
        self.config = {}
        self.update_config()


    def update_config(self):
        self.config['xmin'] = self.xmin.get_value()
        self.config['xmax'] = self.xmax.get_value()
        self.config['Gmin'] = self.Gmin.get_value()
        self.config['Gmax'] = self.Gmax.get_value()
        self.config['nGbins'] = self.nGbins.get_value()
        self.config['nDbins'] = self.nXbins.get_value()

    def update_config_with_data(self, data):
        self.xmin.update_or_dflt(data.get('xmin'))
        self.xmax.update_or_dflt(data.get('xmax'))
        self.Gmin.update_or_dflt(data.get('Gmin'))
        self.Gmax.update_or_dflt(data.get('Gmax'))
        self.nGbins.update_or_dflt(data.get('nGbins'))
        self.nXbins.update_or_dflt(data.get('nDbins'))

        self.update_config()

    def get_config(self):
        self.update_config()
        return self.config

    def get_xmin(self):
        return self.xmin.get_value()
    def get_xmax(self):
        return self.xmax.get_value()
    def get_Gmin(self):
        return self.Gmin.get_value()
    def get_Gmax(self):
        return self.Gmax.get_value()
    def get_nGbins(self):
        return self.nGbins.get_value()
    def get_nXbins(self):
        return self.nXbins.get_value()

class save_options(object):
    def __init__(self, data=None):
        self.build_config_dflt()
        if data:
            self.update_config_with_data(data)

    def build_config_dflt(self):
        date = time.strftime("%Y%m%d_%H%M%S")
        self.save_dir = param.save_dir()
        self.save_data = param.save_data()
        self.use_json = param.use_json()
        self.traces = param.traces()
        self.dflt_filename = "scan_{0}".format(date)
        self.config = {}
        self.update_config()


    def update_config(self):
        self.config['SaveData'] = self.save_data.get_value()
        self.config['SaveDir'] = self.save_dir.get_value()
        self.config['UseJson'] = self.use_json.get_value()
        self.config['NumberTraces'] = self.traces.get_value()

    def update_config_with_data(self, data):
        self.save_dir.update(data.get('SaveDir'))
        self.save_data.update(data.get('SaveData'))
        self.use_json.update(data.get('UseJson'))
        self.traces.update_or_dflt(data.get('NumberTraces'))

        self.update_config()

    def get_config(self):
        self.update_config()
        return self.config

    def get_save_data(self):
        return self.save_data.get_value()
    def get_save_dir(self):
        return self.save_dir.get_value()

    def get_use_json(self):
        return self.use_json.get_value()
    def get_filename(self):
        return self.dflt_filename
    def get_traces(self):
        return self.traces.get_value()

def yaml_loader(filepath):
    with open(filepath, "r") as file_descriptor:
        data = yaml.safe_load(file_descriptor)
    return data

def yaml_dump(filepath, data):
    with open(filepath, "w") as file_descriptor:
        yaml.dump(data, file_descriptor, default_flow_style=False)

def yaml_build_config_from_file(filepath):
    data = yaml_loader(filepath)
    return program_config(data)
