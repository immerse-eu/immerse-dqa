# Required Libraries
import pandas as pd
from functools import reduce
from tabulate import tabulate
from pandas import DataFrame
import numpy as np

# Function to generate aggregated status/count information for each site, visit and form to be visualized on the dashboard
def prepareDashboard(config, dfMaganamed):

    # Initialize dataframe for dashboard
    dfDashboard: DataFrame = pd.DataFrame(columns = ["datasource", "ecrf_acronym", "center_name", "visit_name", "participant_identifier", "ecrf_status", "ecrf_fillouttime", "included_in_study"])

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

    # Add column for included status for all participant_identifiers
    df = pd.DataFrame(columns=["participant_identifier", "included_in_study"])
    df["participant_identifier"] = dfMaganamed["SCREENING"]["participant_identifier"]
    df["included_in_study"] = dfMaganamed["SCREENING"]["SCREENING_decision"]
    dfDashboard = pd.merge(dfDashboard, df, how="left", on=["participant_identifier"])

    #Remove second column after merge for included data without information
    dfDashboard.drop(['included_in_study_x'], axis=1, inplace=True)
    dfDashboard.rename({'included_in_study_y': 'included_in_study'}, axis=1, inplace=True)

    # Map values of included column to human-interpretable codes
    dictRemap = {0.0: "not_included",
                 1.0: "included"}
    dfDashboard.replace({"included_in_study": dictRemap}, inplace=True)

    # Add additional column for participants_center (Site) to get both Lothian centers separated
    df = pd.DataFrame(columns=["participant_identifier", "Site"])
    df["participant_identifier"] = dfMaganamed["KINDPARTI"]["participant_identifier"]
    df["Site"] = dfMaganamed["KINDPARTI"]["KINDPARTI_Site"]
    dfDashboard = pd.merge(dfDashboard, df, how="left", on=["participant_identifier"])
    # Map values of Site column to human-interpretable codes
    dictRemap = {1.0: "Lothian",
                 2.0: "Lothian CAMSH",
                 3.0: "Mannheim",
                 4.0: "Wiesloch",
                 5.0: "Leuven",
                 6.0: "Bierbeek",
                 7.0: "Bratislava",
                 8.0: "Kosice"}
    dfDashboard.replace({"Site": dictRemap}, inplace=True)

    # Change values of center_name based on Site to separate Lothian and Lothian CAMSH
    # only change center_name from Lothian to Lothian CAMSH, if Lothian is set in center_name and Lothian CAMSH in Site column
    # do not change if center_name is Main (test site)
    mask = (dfDashboard.Site == 'Lothian CAMSH') & (dfDashboard.center_name == "Lothian")
    dfDashboard["center_name"][mask] = "Lothian_CAMSH"


    # Return dataframe with dashboard data
    return(dfDashboard)
