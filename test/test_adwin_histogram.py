# [[file:~/Lab_Diana/Programa_python/MCBJ-Control-Program/Measure_samples.org::*ADwin%20Histogram%20testing][ADwin Histogram testing:1]]
from time import strftime
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import sys
sys.path.append("../")
from modules.adwin_driver import *
from modules.configuration import *


# Configure Plot
infile = "Measurement_deafult_config.yaml"
outfile = "Measurement_read_config.yaml"
config = yaml_build_config_from_file(infile)
dconfig = config.display_config
hconfig = config.hist_config


adw = adwin_hist_driver(hconfig)
date = strftime("%y%m%d")
break_histogram, make_histogram = adw.measure_and_get_histogram()
break_histogram.print_histogram()
# ADwin Histogram testing:1 ends here
