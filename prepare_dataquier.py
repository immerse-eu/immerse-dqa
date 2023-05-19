# Required Libraries
import yaml
import os.path as p
import codecs
import pandas as pd
from functools import reduce

from pandas import DataFrame
from tabulate import tabulate

# Function to prepare metadata for quality analysis in dataquieR
def prepareDataquier(config, dictCodebook, dataframesMaganamed):

    # Merge all dataframes into a single dataframe, with outer join on participant_id, center_name and visit_name
    dataFrames = []
    for ecrfAcronym in dataframesMaganamed:
        dataFrames.append(dataframesMaganamed[ecrfAcronym])
    df_merged = reduce \
        (lambda left, right: pd.merge(left, right, on=["participant_identifier", "center_name", "visit_name"], how="outer"), dataFrames)

    # Export merged dataframe to CSV file
    df_merged.to_csv(config["localPaths"]["basePathDqa"] + "/eq5d5l1_data.csv", sep = ";", index = False)

    # Initialize dataquieR metadata with default fields
    dqMetadata: DataFrame = pd.DataFrame(
        columns=['VAR_NAMES', 'LABEL', 'DATA_TYPE', 'VALUE_LABELS', 'MISSING_LIST', 'JUMP_LIST', 'HARD_LIMITS',
                 'DETECTION_LIMITS', 'CONTRADICTIONS', 'SOFT_LIMITS', 'DISTRIBUTION', 'DECIMALS',
                 'DATA_ENTRY_TYPE', 'KEY_OBSERVER', 'KEY_DEVICE', 'KEY_DATETIME', 'KEY_STUDY_SEGMENT',
                 'VARIABLE_ROLE', 'VARIABLE_ORDER', 'LONG_LABEL'])
    dqMetadata = dqMetadata.append({'VAR_NAMES': 'participant_identifier',
                                    'LABEL': 'participant_identifier',
                                    'DATA_TYPE': 'string',
                                    'VALUE_LABELS': '',
                                    'MISSING_LIST': '',
                                    'JUMP_LIST': '',
                                    'HARD_LIMITS': '',
                                    'DETECTION_LIMITS': '',
                                    'CONTRADICTIONS': '',
                                    'SOFT_LIMITS': '',
                                    'DISTRIBUTION': '',
                                    'DECIMALS': '',
                                    'DATA_ENTRY_TYPE': '',
                                    'KEY_OBSERVER': '',
                                    'KEY_DEVICE': '',
                                    'KEY_DATETIME': '',
                                    'KEY_STUDY_SEGMENT': '',
                                    'VARIABLE_ROLE': '',
                                    'VARIABLE_ORDER': '',
                                    'LONG_LABEL': 'participant_identifier'}, ignore_index=True)
    dqMetadata = dqMetadata.append({'VAR_NAMES': 'center_name',
                                    'LABEL': 'center_name',
                                    'DATA_TYPE': 'string',
                                    'VALUE_LABELS': '',
                                    'MISSING_LIST': '',
                                    'JUMP_LIST': '',
                                    'HARD_LIMITS': '',
                                    'DETECTION_LIMITS': '',
                                    'CONTRADICTIONS': '',
                                    'SOFT_LIMITS': '',
                                    'DISTRIBUTION': '',
                                    'DECIMALS': '',
                                    'DATA_ENTRY_TYPE': '',
                                    'KEY_OBSERVER': '',
                                    'KEY_DEVICE': '',
                                    'KEY_DATETIME': '',
                                    'KEY_STUDY_SEGMENT': '',
                                    'VARIABLE_ROLE': '',
                                    'VARIABLE_ORDER': '',
                                    'LONG_LABEL': 'center_name'}, ignore_index=True)
    dqMetadata = dqMetadata.append({'VAR_NAMES': 'visit_name',
                                    'LABEL': 'visit_name',
                                    'DATA_TYPE': 'string',
                                    'VALUE_LABELS': '',
                                    'MISSING_LIST': '',
                                    'JUMP_LIST': '',
                                    'HARD_LIMITS': '',
                                    'DETECTION_LIMITS': '',
                                    'CONTRADICTIONS': '',
                                    'SOFT_LIMITS': '',
                                    'DISTRIBUTION': '',
                                    'DECIMALS': '',
                                    'DATA_ENTRY_TYPE': '',
                                    'KEY_OBSERVER': '',
                                    'KEY_DEVICE': '',
                                    'KEY_DATETIME': '',
                                    'KEY_STUDY_SEGMENT': '',
                                    'VARIABLE_ROLE': '',
                                    'VARIABLE_ORDER': '',
                                    'LONG_LABEL': 'visit_name'}, ignore_index=True)

    # Walk through fields of eCRF(s) and add metadata rows
    for ecrfId in dictCodebook["eCRFs"]:
        ecrfAcronym = dictCodebook["eCRFs"][ecrfId]["ecrfAcronym"]
        if ecrfAcronym.startswith("EQ5D5L1"):

            # Add default metadata fields specific to current eCRF
            dqMetadata = dqMetadata.append({'VAR_NAMES': ecrfAcronym + '_started_at',
                                            'LABEL': ecrfAcronym + '_started_at',
                                            'DATA_TYPE': 'datetime',
                                            'VALUE_LABELS': '',
                                            'MISSING_LIST': '',
                                            'JUMP_LIST': '',
                                            'HARD_LIMITS': '',
                                            'DETECTION_LIMITS': '',
                                            'CONTRADICTIONS': '',
                                            'SOFT_LIMITS': '',
                                            'DISTRIBUTION': '',
                                            'DECIMALS': '',
                                            'DATA_ENTRY_TYPE': '',
                                            'KEY_OBSERVER': '',
                                            'KEY_DEVICE': '',
                                            'KEY_DATETIME': '',
                                            'KEY_STUDY_SEGMENT': '',
                                            'VARIABLE_ROLE': '',
                                            'VARIABLE_ORDER': '',
                                            'LONG_LABEL': ecrfAcronym + '_started_at'}, ignore_index=True)
            dqMetadata = dqMetadata.append({'VAR_NAMES': ecrfAcronym + '_finished_at',
                                            'LABEL': ecrfAcronym + '_finished_at',
                                            'DATA_TYPE': 'datetime',
                                            'VALUE_LABELS': '',
                                            'MISSING_LIST': '',
                                            'JUMP_LIST': '',
                                            'HARD_LIMITS': '',
                                            'DETECTION_LIMITS': '',
                                            'CONTRADICTIONS': '',
                                            'SOFT_LIMITS': '',
                                            'DISTRIBUTION': '',
                                            'DECIMALS': '',
                                            'DATA_ENTRY_TYPE': '',
                                            'KEY_OBSERVER': '',
                                            'KEY_DEVICE': '',
                                            'KEY_DATETIME': '',
                                            'KEY_STUDY_SEGMENT': '',
                                            'VARIABLE_ROLE': '',
                                            'VARIABLE_ORDER': '',
                                            'LONG_LABEL': ecrfAcronym + '_finished_at'}, ignore_index=True)
            dqMetadata = dqMetadata.append({'VAR_NAMES': ecrfAcronym + '_status',
                                            'LABEL': ecrfAcronym + '_status',
                                            'DATA_TYPE': 'string',
                                            'VALUE_LABELS': 'EMPTY = Empty | STARTED = Started | COMPLETED = Completed',
                                            'MISSING_LIST': '',
                                            'JUMP_LIST': '',
                                            'HARD_LIMITS': '',
                                            'DETECTION_LIMITS': '',
                                            'CONTRADICTIONS': '',
                                            'SOFT_LIMITS': '',
                                            'DISTRIBUTION': '',
                                            'DECIMALS': '',
                                            'DATA_ENTRY_TYPE': '',
                                            'KEY_OBSERVER': '',
                                            'KEY_DEVICE': '',
                                            'KEY_DATETIME': '',
                                            'KEY_STUDY_SEGMENT': '',
                                            'VARIABLE_ROLE': '',
                                            'VARIABLE_ORDER': '',
                                            'LONG_LABEL': ecrfAcronym + '_status'}, ignore_index=True)
            dqMetadata = dqMetadata.append({'VAR_NAMES': ecrfAcronym + '_fillouttime',
                                            'LABEL': ecrfAcronym + '_fillouttime',
                                            'DATA_TYPE': 'float',
                                            'VALUE_LABELS': '',
                                            'MISSING_LIST': '',
                                            'JUMP_LIST': '',
                                            'HARD_LIMITS': '',
                                            'DETECTION_LIMITS': '',
                                            'CONTRADICTIONS': '',
                                            'SOFT_LIMITS': '',
                                            'DISTRIBUTION': '',
                                            'DECIMALS': '',
                                            'DATA_ENTRY_TYPE': '',
                                            'KEY_OBSERVER': '',
                                            'KEY_DEVICE': '',
                                            'KEY_DATETIME': '',
                                            'KEY_STUDY_SEGMENT': '',
                                            'VARIABLE_ROLE': '',
                                            'VARIABLE_ORDER': '',
                                            'LONG_LABEL': ecrfAcronym + '_fillouttime'}, ignore_index=True)

            # Walk through fields of form within codebook
            for itemId in dictCodebook["eCRFs"][ecrfId]["items"]:
                dataType = ""
                valueLabels = ""
                if dictCodebook["eCRFs"][ecrfId]["items"][itemId]["itemDataType"] == "text":
                    dataType = "string"
                elif dictCodebook["eCRFs"][ecrfId]["items"][itemId]["itemDataType"] == "date":
                    dataType = "datetime"
                elif dictCodebook["eCRFs"][ecrfId]["items"][itemId]["itemDataType"] in ["singleChoice", "multipleChoice"]:
                    dataType = "string"
                    answers = []
                    for answerId in dictCodebook["eCRFs"][ecrfId]["items"][itemId]["answers"]:
                        answers.append \
                            (str(dictCodebook["eCRFs"][ecrfId]["items"][itemId]["answers"][answerId]["answerCode"]) + " = " + dictCodebook["eCRFs"][ecrfId]["items"][itemId]["answers"][answerId]["answerText"])
                    valueLabels = " | ".join(answers)

                dqMetadata = dqMetadata.append \
                    ({'VAR_NAMES': ecrfAcronym + '_' + dictCodebook["eCRFs"][ecrfId]["items"][itemId]["itemCode"],
                                                'LABEL': ecrfAcronym + '_' + dictCodebook["eCRFs"][ecrfId]["items"][itemId]["itemPrompt"],
                                                'DATA_TYPE': dataType,
                                                'VALUE_LABELS': valueLabels,
                                                'MISSING_LIST': '',
                                                'JUMP_LIST': '',
                                                'HARD_LIMITS': '',
                                                'DETECTION_LIMITS': '',
                                                'CONTRADICTIONS': '',
                                                'SOFT_LIMITS': '',
                                                'DISTRIBUTION': '',
                                                'DECIMALS': '',
                                                'DATA_ENTRY_TYPE': '',
                                                'KEY_OBSERVER': '',
                                                'KEY_DEVICE': '',
                                                'KEY_DATETIME': '',
                                                'KEY_STUDY_SEGMENT': '',
                                                'VARIABLE_ROLE': '',
                                                'VARIABLE_ORDER': '',
                                                'LONG_LABEL': dictCodebook["eCRFs"][ecrfId]["items"][itemId]["itemPrompt"]}, ignore_index=True)

    # Export merged dataframe to CSV file
    dqMetadata.to_csv(config["localPaths"]["basePathDqa"] + "/eq5d5l1_meta.csv", sep = ";", index = False)

    print(tabulate(df_merged, headers = "keys"))
    print(tabulate(dqMetadata, headers = "keys"))
