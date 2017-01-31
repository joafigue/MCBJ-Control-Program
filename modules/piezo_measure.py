""" Module - piezo_measure.py : Performs measuremnet with piezo + interface

This file, uses the adwin to perform the histogram measurements
and provides with interface to analyze the results
"""
__author__ = "Joaquin Figueroa"
import pylab as pl
import numpy as np
import matplotlib.pyplot as plt
import os
import json
import modules.parameters as param

class histogram_save_data_class(object):
    def __init__(self, break_histogram, make_histogram, full_config):
        self.full_config = full_config
        self.G_breaking = break_histogram.get_conductance()
        self.V_breaking = break_histogram.get_voltage()
        self.D_breaking = []
        self.T_breaking = []

        self.G_making = make_histogram.get_conductance()
        self.V_making = make_histogram.get_voltage()
        self.D_making = []
        self.T_making = []

        self.convert_break_voltage_to_distance()
        self.generate_break_time_array()

        self.convert_make_voltage_to_distance()
        self.generate_make_time_array()


    def convert_break_voltage_to_distance(self):
        G_array = self.G_breaking
        V_array = self.V_breaking
        d_max_v = param.ADW_GCONST.OUTPUT_MAX_D # nm guess
        max_v = param.ADW_GCONST.OUTPUT_RANGE # Adwin_voltage
        distance = V_array *(d_max_v/max_v)
        real_brk_idx = max(pl.find(G_array > 0.5))
        recentered_distance = distance - distance[real_brk_idx]
        self.D_breaking = recentered_distance

    def convert_make_voltage_to_distance(self):
        G_array = self.G_making
        V_array = self.V_making
        d_max_v = param.ADW_GCONST.OUTPUT_MAX_D # nm guess
        max_v = param.ADW_GCONST.OUTPUT_RANGE # Adwin_voltage
        distance = V_array *(d_max_v/max_v)
        real_mk_idx = min(pl.find(G_array < 0.5))
        recentered_distance = distance - distance[real_mk_idx]
        self.D_making = recentered_distance

    def generate_break_time_array(self):
        hist_config = self.full_config.hist_config
        time_per_point = hist_config.get_time_per_break_data_point()
        length = len(self.G_breaking)
        self.T_breaking = np.array(range(0, length)) * time_per_point


    def generate_make_time_array(self):
        hist_config = self.full_config.hist_config
        time_per_point = hist_config.get_time_per_make_data_point()
        length = len(self.G_making)
        self.T_making = np.array(range(0, length)) * time_per_point

    def get_G_breaking(self):
        return self.G_breaking
    def get_D_breaking(self):
        return self.D_breaking
    def get_V_breaking(self):
        return self.V_breaking
    def get_T_breaking(self):
        return self.T_breaking
    def get_G_making(self):
        return self.G_making
    def get_D_making(self):
        return self.D_making
    def get_V_making(self):
        return self.V_making
    def get_T_making(self):
        return self.T_making

    def save_data(self, trace=1):
        save_config = self.full_config.save_config
        if save_config.get_save_data():
            if save_config.get_use_json():
                self._real_save_data_with_json(trace)
            else:
                self._real_save_data(trace)
    def _real_save_data(self, trace=1):
        save_dir =  self.full_config.save_config.get_save_dir()
        filename = self.full_config.save_config.get_filename()
        filename = "{0}_{1}.dat".format(filename, trace)
        real_filename = os.path.join(save_dir, filename)
        filedesc = open(real_filename, "w")


        self.make_piezo_header(filedesc)
        filedesc.write('@ \n')
        for T, G, V in zip(self.T_breaking, self.G_breaking, self.V_breaking):
            ln = "{0:1.8f}\t{1:1.8f}\t{2:1.8f}\t\n".format(T, G, V)
            filedesc.write(ln)
        filedesc.write('@ \n')
        for T, G, V in zip(self.T_making, self.G_making, self.V_making):
            ln = "{0:1.8f}\t{1:1.8f}\t{2:1.8f}\t\n".format(T, G, V)
            filedesc.write(ln)

    def _real_save_data_with_json(self, trace=1):
        self._real_save_data(trace) # TODO - Actually write

    def make_piezo_header(self, fd):
        hc = self.full_config.hist_config
        fd.write('Juncture voltage : {0} V\n'.format(hc.get_real_jv()))
        fd.write('Breaking speed : {0} V/s\n'.format(hc.break_speed.get_value()))
        fd.write('Making speed : {0} V/s\n'.format(hc.make_speed.get_value()))
        fd.write('Post breaking : {0} V\n'.format(hc.post_breaking_v.get_value()))


class histogram_plot_data_class(object):
    def __init__(self, dconfig):      # display_config
        self.dconfig = dconfig
        nGbins = dconfig.get_nGbins()
        self.Gmax = dconfig.get_Gmax()
        self.Gmin = dconfig.get_Gmin()
        G_powers = np.linspace(np.log10(self.Gmin), np.log10(self.Gmax), nGbins)
        # Conductance bins for histogram
        self.Gbins = np.power(np.zeros(nGbins) + 10.0, G_powers)

        nDbins = dconfig.get_nXbins()
        self.xmin = dconfig.get_xmin()
        self.xmax = dconfig.get_xmax()
        # Displacement bins for histogram
        self.Dbins = np.linspace(self.xmin, self.xmax, nDbins)

        self.histo1D_breaking_sum = np.zeros(nGbins-1)
        self.histo1D_making_sum = np.zeros(nGbins-1)
        self.histo2D_breaking_sum = np.zeros(shape=(nGbins-1, nDbins-1))

        self.prepare_plot_config()
        self.hist_data = None

    def prepare_plot_config(self):
        ## plot settings
        pl.rcParams['figure.figsize'] = [22, 10]
        font = {'family' : 'normal',
                'weight' : 'normal',
                'size'   : 22}
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
        ax1.set_position([0.07, 0.1, 0.25, 0.8])
        ax2.set_position([0.39, 0.1, 0.25, 0.8])
        ax3.set_position([0.72, 0.1, 0.25, 0.8])
        fig.set_facecolor('white')
        pl.matplotlib.rc('font', **font)
        self.figure = fig
        self.break_make_trace = ax1
        self.histogram_1D = ax2
        self.histogram_2D = ax3

    def update_histogram_plt_data(self, histogram_save_data):
        self.hist_data = histogram_save_data
        bins = (self.Gbins, self.Dbins)

        G_breaking = histogram_save_data.get_G_breaking()
        D_breaking = histogram_save_data.get_D_breaking()
        G_making = histogram_save_data.get_G_making()

        break_histogram = pl.histogram(G_breaking, self.Gbins)
        make_histogram = pl.histogram(G_making, self.Gbins)


        self.histo1D_breaking_sum = self.histo1D_breaking_sum + break_histogram[0]
        self.histo1D_making_sum = self.histo1D_making_sum + make_histogram[0]

        break_histogram2D = pl.histogram2d(G_breaking, D_breaking, bins)
        self.histo2D_breaking_sum = self.histo2D_breaking_sum + break_histogram2D[0]

    def plot_break_make_trace(self):
        axis = self.break_make_trace
        axis.clear()
        G_breaking = self.hist_data.get_G_breaking()
        D_breaking = self.hist_data.get_D_breaking()
        G_making = self.hist_data.get_G_making()
        D_making = self.hist_data.get_D_making()

        axis.plot(D_breaking, G_breaking, linewidth=2)
        axis.plot(D_making, G_making, linewidth=2)
        axis.set_yscale("log")
        axis.set_xlim(-5, max(max(D_making), max(D_breaking)))
        axis.set_ylim(self.Gmin, self.Gmax)
        axis.set_title("Conductance trace")
        axis.set_xlabel('Displacement (nm)')
        axis.set_ylabel('Conductance (G0)')
        axis.set_aspect(1)

    def plot_histogram_1D(self):
        axis = self.histogram_1D
        axis.clear()
        Gbins_plot = self.Gbins[:-1]
        axis.plot(Gbins_plot, self.histo1D_breaking_sum, linewidth=2)
        axis.plot(Gbins_plot, self.histo1D_making_sum, linewidth=2)
        y_max = 1.2*max(max(self.histo1D_breaking_sum), max(self.histo1D_making_sum))

        axis.set_xscale("log")
        axis.set_ylim(0, y_max)
        axis.set_xlim(self.Gbins[0], self.Gbins[-1])
        axis.set_title("1D Histogram")
        axis.set_ylabel('Counts')
        axis.set_xlabel('Conductance (G0)')
        axis.set_aspect(1)

    def get_max_counts_in_histogram2D(self):
        high_Gbins = abs(np.log10(self.Gbins) - -2)
        low_Gbins = abs(np.log10(self.Gbins) - -6)
        low_idx = pl.find(min(low_Gbins) == low_Gbins)[0]
        high_idx = pl.find(min(high_Gbins) == high_Gbins)[0]
        tmp = self.histo2D_breaking_sum[low_idx:high_idx, :]
        Cmax = 0
        for y in range(0, high_idx - low_idx):
            Cmax = max(max(tmp[y, :]), Cmax)
        return int(Cmax)

    def plot_histogram_2D(self):
        axis = self.histogram_2D
        Gbins_plot = self.Gbins[:-1]
        Dbins_plot = self.Dbins[:-1]
        max_counts = self.get_max_counts_in_histogram2D()
        levels = np.linspace(0, max_counts/2, 16)
        axis.clear()
        axis.contourf(Dbins_plot, Gbins_plot, self.histo2D_breaking_sum, levels)
        axis.set_yscale("log")
        axis.set_ylim(Gbins_plot[0], Gbins_plot[-1])
        axis.set_xlim(Dbins_plot[0], Dbins_plot[-1])
        axis.set_title("2D Histogram")
        axis.set_xlabel('Displacement (nm)')
        axis.set_ylabel('Conductance (G0)')
