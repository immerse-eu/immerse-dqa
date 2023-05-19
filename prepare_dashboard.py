# Required Libraries
import pandas as pd
from functools import reduce
from tabulate import tabulate

# Function to generate aggregated status/count information for each site, visit and form to be visualized on the dashboard
def prepareDashboard(config, dfMaganamed):

    # Initialize dataframe for dashboard
    dfDashboard: DataFrame = pd.DataFrame(columns=["ecrf_acronym", "center_name", "visit_name", "ecrf_status", "n"])

    # Walk through eCRFs
    for ecrfAcronym in dfMaganamed:

        print(ecrfAcronym)

        dfAgg = dfMaganamed[ecrfAcronym].groupby("center_name", "visit_name", "ecrf_status").size()

        print(tabulate(dfAgg, headers="keys"))