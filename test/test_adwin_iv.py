# [[file:~/Lab_Diana/Programa_python/joaquin_rewrite/Measure_samples.org::*Adwin%20IV%20testing][Adwin IV testing:1]]
from time import strftime
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from modules.adwin_driver import *
from modules.configuration import *


# Configure Plot
infile = "Measurement_deafult_config.yaml"
outfile = "Measurement_read_config.yaml"
config = yaml_build_config_from_file(infile)
dconfig = config.display_config
hconfig = config.hist_config
iv_config = config.iv_config


adw = adwin_iv_driver(iv_config)
adw.start_process()
adw.analyze()
for i in range(100):
    print(adw.get_conductance())
# Adwin IV testing:1 ends here
