# Required Libraries
# - install packages: PyYAML
import os
import yaml
import pandas as pd
from tabulate import tabulate
from functools import reduce

# Required modules
import prepare_dashboard
import prepare_dataquier



# Required modules
import maganamed

# Read configuration file
with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# Compile Maganamed dataframes
dfMaganamed = maganamed.compileMaganamedData(config)

prepareDashboard(config, dfMaganamed)




