import sys
sys.path.append("../")
import modules.piezo_measure as pm
import modules.adwin_driver as adw
import modules.configuration as conf
import matplotlib.pyplot as plt
import modules.faulhaber_driver as fh

def stop():
    motor = fh.faulhaber_motor()
    motor.enable_motor()
    motor.stop_motor()
    motor.disable_motor()
    adw.adwin_driver(1, "")


# Configure Plot
infile = "Measurement_deafult_config.yaml"
outfile = "Measurement_read_config.yaml"
config = conf.yaml_build_config_from_file(infile)
dconfig = config.display_config
hconfig = config.hist_config
iv_config = config.iv_config


adw_hist = adw.adwin_hist_driver(hconfig)
hist_plotter = pm.histogram_plot_data_class(dconfig)

for trace in range(10):
    break_hist, make_hist = adw_hist.measure_and_get_histogram(trace)
    hist_save = pm.histogram_save_data_class(break_hist, make_hist, config)
    hist_save.save_data(trace)
    hist_plotter.update_histogram_plt_data(hist_save)
    hist_plotter.plot_break_make_trace()
    hist_plotter.plot_histogram_1D()
    hist_plotter.plot_histogram_2D()
