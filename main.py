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
import dashboard_visualization

# Required modules
import maganamed

# Read configuration file
with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# Compile Maganamed dataframes
dfMaganamed = maganamed.compileMaganamedData(config)

#print(tabulate(dfMaganamed["EQ5D5L1"], headers="keys"))

dfDashboard = prepare_dashboard.prepareDashboard(config, dfMaganamed)

# Export merged dataframe to CSV file
dfDashboard.to_csv(config["localPaths"]["basePathDqa"] + "/dashboard.csv", sep = ";", index = False)

# generate dashboard figures
dashboard_visualization.prepareFigures(config, dfDashboard)
