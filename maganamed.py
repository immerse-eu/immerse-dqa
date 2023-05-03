# Required Libraries
import yaml
import os.path as p
import codecs
import pandas as pd

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

    print("File headers")
    for ecrfId in dictCodebook["eCRFs"]:
        ecrfFilename = dictCodebook["eCRFs"][ecrfId]["ecrfFilename"]
        if p.isfile(config["localPaths"]["basePathMaganamed"] + "/export/" + ecrfFilename):
            with open(config["localPaths"]["basePathMaganamed"] + "/export/" + ecrfFilename, 'r', encoding='utf-8-sig') as file:
                first_line = file.readline()
                print(f"{ecrfFilename}\t{first_line}")

    # Load CSV exports for eCRFs into a dictionary
#    dataframesMaganamed = {}
#    for ecrfId in dictCodebook["eCRFs"]:
#        ecrfFilename = dictCodebook["eCRFs"][ecrfId]["ecrfFilename"]
#        ecrfAcronym = dictCodebook["eCRFs"][ecrfId]["ecrfAcronym"]
#        if p.isfile(config["localPaths"]["basePathMaganamed"] + "/export/" + ecrfFilename):
#            if ecrfAcronym.startswith("EQ"):
#                print(str(ecrfId) + ": " + ecrfAcronym + " (" + ecrfFilename + ")")
#                dataframesMaganamed[ecrfAcronym] = pd.read_csv(config["localPaths"]["basePathMaganamed"] + "/export/" + ecrfFilename)

#    print(dataframesMaganamed)