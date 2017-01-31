import sys
sys.path.append("../")
import modules.parameters as param
log_ampl = param.adwin_log_amplifier()
calibration = log_ampl.get_calibration()
print calibration
