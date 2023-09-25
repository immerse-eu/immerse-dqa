# Required Libraries
import pandas as pd
from functools import reduce
from tabulate import tabulate
from pandas import DataFrame
import numpy as np
import os
import os.path as p

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
    df["visit_name"] = dfMaganamed["SCREENING"]["visit_name"]
    df = df[df.visit_name == "Screening"]
    df.drop(['visit_name'], axis=1, inplace=True)
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

# Function to check individual response rate of certain ecrfs
def approximateReponsePercent(config, dfDashboard, created_date):
    file_path = config["localPaths"]["basePathMaganamed"] + "/export/"
    responseInfo_all = pd.DataFrame()
    # list of ecrfs to process
    fileNames_to_check = ['Demographics-(Clinicians).csv', 'Demographics-(Patients).csv', 'Service-Attachement-Questionnaire-(SAQ).csv']
    ecrfAcronyms_to_check = ['DEMOG_CLIN', 'DEMOG_PAT', 'SAQ']
    i = 0
    # process for each ecrf: check the response status beyond all participants
    for file_name in fileNames_to_check:
        file_path = os.path.join(file_path, file_name)
        # read CSV to dataframe
        if p.isfile(config["localPaths"]["basePathMaganamed"] + "/export/" + file_name):
            df = pd.read_csv(config["localPaths"]["basePathMaganamed"] + "/export/" + file_name, delimiter=";")
        # add & remove columns
        df['ecrf_acronym'] = ecrfAcronyms_to_check[i]
        i += 1
        df['responsed_items'] = 0
        df['responsePercent_approx'] = None
        df['responsePercent'] = None
        df['unresponsed_variables'] = "" # [] oder null?
        df = df.drop(['created_at', 'diary_date'], axis=1)
        # define question columns to check
        question_columns = [col for col in df.columns if
                            col not in ['participant_identifier', 'center_name', 'ecrf_acronym', 'started_at',
                                        'finished_at', 'visit_name', 'responsed_items', 'responsePercent',
                                        'responsePercent_approx', 'unresponsed_variables']]
        # process for each participant: check response status & update columns 'responsed_items'과 'unresponsed_variables'
        for index, row in df.iterrows():
            # count responsed items & save in column 'responsed_items'
            response_count = sum([1 for col in question_columns if not pd.isnull(row[col])])
            df.at[index, 'responsed_items'] = int(response_count)
            df['responsed_items'] = df['responsed_items'].astype(int)
            # extract all variable names of unresponsed items & save in column 'unresponsed_variables'
            unresponsed_vars = [col for col in question_columns if pd.isnull(row[col])]
            df.at[index, 'unresponsed_variables'] = ', '.join(unresponsed_vars)
            # for better concise visualization
            df.loc[df['responsed_items'] == 0, 'unresponsed_variables'] = 'all variables are not responsed'
        # calculate response rate as percentage
        if (df['ecrf_acronym'] == 'DEMOG_CLIN').all():
            result = df['responsed_items'] / 14
        elif (df['ecrf_acronym'] == 'DEMOG_PAT').all():
            result = df['responsed_items'] / 19
        elif (df['ecrf_acronym'] == 'SAQ').all():
            result = df['responsed_items'] / 25
        # save response percentage in appropriate columns
        if file_name in ['Demographics-(Clinicians).csv', 'Demographics-(Patients).csv']:
            df['responsePercent_approx'] = round(result * 100, 2)
            df.loc[df['responsePercent_approx'] > 100,'responsePercent_approx'] = 100
        else:
            df['responsePercent'] = round(result * 100, 2)
        # Merge all columns in one dataframe
        responseInfo_all = pd.concat(
            [responseInfo_all, df[['participant_identifier', 'center_name', 'ecrf_acronym', 'visit_name', 'responsed_items', 'responsePercent', 'responsePercent_approx', 'unresponsed_variables']]],
            ignore_index=True)
        responseInfo_all.to_excel(config["localPaths"]["basePathDqa"] + "/maganamed_responseTableXLSX_createdOn_" + created_date + ".xlsx", index = False)
        responseInfo_all.to_csv(config["localPaths"]["basePathDqa"] + "/maganamed_responseTableCSV_createdOn_" + created_date + ".csv", sep = ";", index = False)




    # merge response information into dfDashboard
    dfDashboard = pd.merge(dfDashboard, responseInfo_all[
        ['participant_identifier', 'ecrf_acronym', 'visit_name', 'responsed_items', 'responsePercent', 'responsePercent_approx', 'unresponsed_variables']],
                           on=['participant_identifier', 'ecrf_acronym', 'visit_name'], how='left')
    return(dfDashboard)
