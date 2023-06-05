# Required Libraries
import yaml
import os.path as p
import codecs
import pandas as pd
from functools import reduce

from pandas import DataFrame
from tabulate import tabulate

# Function to compile dataframes for data quality analysis from Maganamed codebook and CSV export files
def compileMaganamedData(config):

    # Read parsed Maganamed Codebook
    with open(config["localPaths"]["basePathMaganamed"] + "/codebook.yaml", "r") as f:
        dictCodebook = yaml.load(f, Loader=yaml.FullLoader)

#    # Find eCRFs with missing CSV files
#    print("Missing files")
#    for ecrfId in dictCodebook["eCRFs"]:
#        ecrfFilename = dictCodebook["eCRFs"][ecrfId]["ecrfFilename"]
#        if not p.isfile(config["localPaths"]["basePathMaganamed"] + "/export/" + ecrfFilename):
#            print(str(ecrfId) + " " + ecrfFilename)

#    print("File headers")
#    for ecrfId in dictCodebook["eCRFs"]:
#        ecrfFilename = dictCodebook["eCRFs"][ecrfId]["ecrfFilename"]
#        if p.isfile(config["localPaths"]["basePathMaganamed"] + "/export/" + ecrfFilename):
#            with open(config["localPaths"]["basePathMaganamed"] + "/export/" + ecrfFilename, 'r', encoding='utf-8-sig') as file:
#                first_line = file.readline()
#                print(f"{ecrfFilename}\t{first_line}")

    # Load CSV exports for all eCRFs into a dictionary
    dfMaganamed = {}
    for ecrfId in dictCodebook["eCRFs"]:
        ecrfFilename = dictCodebook["eCRFs"][ecrfId]["ecrfFilename"]
        ecrfAcronym = dictCodebook["eCRFs"][ecrfId]["ecrfAcronym"]
        if p.isfile(config["localPaths"]["basePathMaganamed"] + "/export/" + ecrfFilename):
            dfMaganamed[ecrfAcronym] = pd.read_csv(config["localPaths"]["basePathMaganamed"] + "/export/" + ecrfFilename, delimiter = ";")

    # Drop irrelevant columns created_at and diary_date
    for ecrfAcronym in dfMaganamed:
        dfMaganamed[ecrfAcronym].drop(["created_at", "diary_date"], axis = 1, inplace = True)

    # Add status attribute for each row of each eCRF
    for ecrfAcronym in dfMaganamed:
        dfMaganamed[ecrfAcronym]["status"] = dfMaganamed[ecrfAcronym].apply(lambda x: deriveRecordStatus(x.started_at, x.finished_at), axis = 1)

    # Calculate duration of filling out for all completed forms
    for ecrfAcronym in dfMaganamed:
        dfMaganamed[ecrfAcronym]["fillouttime"] = dfMaganamed[ecrfAcronym].apply(lambda x: deriveFilloutTime(x.status, x.started_at, x.finished_at), axis = 1)

    # Prefix column names of non-metadata columns with eCRF acronym
    for ecrfAcronym in dfMaganamed:
        dictRename = {}
        for key in dfMaganamed[ecrfAcronym].keys():
            if key not in ["participant_identifier", "center_name", "visit_name"]:
                dictRename[key] = ecrfAcronym + "_" + key
        dfMaganamed[ecrfAcronym] = dfMaganamed[ecrfAcronym].rename(columns = dictRename)

    # Return dictionary with loaded CSV exports and extended status/duration fields
    return(dfMaganamed)

# Function to calculate eCRF record status based on metadata timestamps
def deriveRecordStatus(timestamp_started, timestamp_finished):
    status = "EMPTY"
    if not pd.isna(timestamp_finished):
        status = "COMPLETED"
    elif not pd.isna(timestamp_started):
        status = "STARTED"
    return(status)

# Function to calculate eCRF fillout duration for completed forms
def deriveFilloutTime(status, timestamp_started, timestamp_finished):
    if status == "COMPLETED":
        td = pd.to_datetime(timestamp_finished) - pd.to_datetime(timestamp_started)
        return(td.seconds)
    else:
        return(None)