# Required Libraries
# - install packages: PyYAML
import os
import yaml

# Required modules
import maganamed

# Read configuration file
with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# Compile Maganamed dataframes
maganamed.compileMaganamedData(config)

# List Contents of export CSV directory
#list = os.listdir(config["localPaths"]["basePathMaganamed"] + "/export")
#print(list)
