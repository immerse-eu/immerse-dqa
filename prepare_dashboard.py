# Required Libraries
import pandas as pd
from functools import reduce
from tabulate import tabulate
from pandas import DataFrame

# Function to generate aggregated status/count information for each site, visit and form to be visualized on the dashboard
def prepareDashboard(config, dfMaganamed):

    # Initialize dataframe for dashboard
    dfDashboard: DataFrame = pd.DataFrame(columns = ["datasource", "ecrf_acronym", "center_name", "visit_name", "participant_identifier", "ecrf_status", "ecrf_fillouttime"])

    # Walk through eCRFs
    for ecrfAcronym in dfMaganamed:

        # Select & rename relevant columns of current eCRF dataframe
        dictRemap = {"center_name": "center_name",
                     "visit_name": "visit_name",
                     "participant_identifier": "participant_identifier",
                     ecrfAcronym+"_status": "ecrf_status",
                     ecrfAcronym+"_fillouttime": "ecrf_fillouttime"}
        df = dfMaganamed[ecrfAcronym].rename(columns = dictRemap)[dictRemap.values()]
        df["datasource"] = "Maganamed"
        df["ecrf_acronym"] = ecrfAcronym

        # Add selected columns of current eCRF to dashboard dataframe
        dfDashboard = pd.concat([dfDashboard, df])

    # Return dataframe with dashboard data
    return(dfDashboard)
