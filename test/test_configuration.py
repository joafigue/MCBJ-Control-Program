import json
import sys
sys.path.append("../")
import modules.configuration as conf

# Configure Plot
infile = "Measurement_deafult_config.yaml"
outfile = "Measurement_read_config.yaml"
config = conf.yaml_build_config_from_file(infile)
dconfig = config.display_config
hconfig = config.hist_config
iv_config = config.iv_config

config.dump_config_file(outfile)


real_config  = config.get_config()
config.dump_config_file(outfile)

dump_file = open(outfile, "a")
dump_file.write("testing\n")
dump_file.close()

json_file = open("json_test.json", "w")
json.dump(real_config, json_file, indent = 4)
asdf = {"break_data" : [1, 2, 3, 4]}
json.dump(asdf, json_file, indent = 4)
json_file.close()
