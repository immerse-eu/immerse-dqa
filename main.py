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
import dashboard_visualization_movisensxs

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
responseInfo_all = prepare_dashboard.approximateReponsePercent(config, dfDashboard, created_date)

# Export merged dataframe to CSV file
dfDashboard.to_csv(config["localPaths"]["basePathDqa"] + "/maganamed_dashboard_createdOn_" + created_date + ".csv", sep = ";", index = False)

# Generate dashboard figures
dashboard_visualization_maganamed.prepareFigures(config, dfDashboard)
dashboard_visualization_maganamed.responsePerParticipants(config, responseInfo_all, created_date)
dashboard_visualization_movisensxs.prepareFigures(config)
