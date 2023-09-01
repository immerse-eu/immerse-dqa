# Required Libraries
# - install packages: PyYAML
import os
import yaml
import pandas as pd
from tabulate import tabulate
from functools import reduce
from datetime import datetime

# Required modules
import prepare_dashboard
import prepare_dataquier
import dashboard_visualization_maganamed
import dashboard_visualization_movisensxs02

# Required modules
import maganamed

# Preparation for file naming
today = datetime.today()
created_date = today.strftime('%Y-%m-%d')

# Read configuration file
with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# Compile Maganamed dataframes
dfMaganamed = maganamed.compileMaganamedData(config)

#print(tabulate(dfMaganamed["EQ5D5L1"], headers="keys"))

dfDashboard = prepare_dashboard.prepareDashboard(config, dfMaganamed)

# Export merged dataframe to CSV file
dfDashboard.to_csv(config["localPaths"]["basePathDqa"] + "/maganamed_dashboard" + created_date + ".csv", sep = ";", index = False)

# generate dashboard figures
dashboard_visualization_maganamed.prepareFigures(config, dfDashboard)
dashboard_visualization_movisensxs02.prepareFigures(config)
