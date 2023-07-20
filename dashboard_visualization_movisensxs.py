# --- Required Libraries
# install packages: os, pandas, numpy, os, openpyxl
import os
import pandas as pd
import numpy as np
import openpyxl

# Preparation
pd.set_option('display.max_columns', None)
# initialize emtpy DataFrame
result_df = pd.DataFrame()
# set different movisensXS databases (folders in exported movisensXS data)
COUNTRY_NAME = ['BE', 'GE', 'UK', 'SK_Female', 'SK', 'SK_Kosice_Female', 'SK_Kosice']

def prepareFigures(config):
    folder_movisensxs = config["localPaths"]["basePathMovisensXS"]
    dqa_folder = config["localPaths"]["basePathDqa"]
    # initialize Excel writer to write Excel file with multiple sheets
    writer = pd.ExcelWriter(dqa_folder + f'/movisensXS_dashboard.xlsx')

    for cntr in COUNTRY_NAME:
        print(f'----- Now start to process {cntr} -----')
        for visitNr in range(4):
            folder_name = f'IMMERSE_T{visitNr}_{cntr}'
            folder_path = folder_movisensxs + '/' + folder_name

            if os.path.isdir(folder_path):  # To check if export has worked properly
                # Extract data from excel files as DataFrame
                excel_file_path = folder_path + '/' + f'{folder_name}.xlsx'
                origin_excel_df = pd.read_excel(excel_file_path)
                df_visitName = origin_excel_df.query('Form == "Initial"')[['participant_id', 'Participant', 'Form']]
                df_visitName = df_visitName.rename(columns={'Participant':f'movi_id_T{visitNr}'})

                # Create a new column about visit (data available: 1)
                df_visitName[f'T{visitNr}'] = np.where(df_visitName['Form'] == "Initial", 1, None)
                df_visitName = df_visitName.drop(columns='Form')

                # Find center name
                if visitNr == 0:
                    print('T0, finding center name')
                    df_visitName = add_center_name(df_visitName)
                    df_T0 = df_visitName.sort_values(by='centerName', ascending=False)
                    result_df = df_T0.copy()
                    print(f'done in {folder_name}')

                else:
                    if visitNr == 1:
                        df_T1 = df_visitName.copy()
                        result_df = pd.merge(result_df, df_T1, how='outer', on='participant_id')
                        print(f'done in {folder_name}')

                    elif visitNr == 2:
                        df_T2 = df_visitName.copy()
                        result_df = pd.merge(result_df, df_T2, how='outer', on='participant_id')
                        print(f'done in {folder_name}')

                    elif visitNr == 3:
                        df_T3 = df_visitName.copy()
                        result_df = pd.merge(result_df, df_T3, how='outer', on='participant_id')
                        print(f'done in {folder_name}')

        # Merging SK Female and Male
        if cntr == 'SK_Female':
            result_SK_Female_df = result_df.copy()
        elif cntr == 'SK':
            result_df =  pd.concat([result_SK_Female_df,result_df])
        elif cntr == 'SK_Kosice_Female':
            result_SK_Kosice_Female_df = result_df.copy()
        elif cntr == 'SK_Kosice':
            result_df =  pd.concat([result_SK_Kosice_Female_df,result_df])


        # Adjust columns of result DataFrame & save as excel
        result_df = result_df[['participant_id', 'centerName', 'T0', 'T1', 'T2', 'T3',
                               'movi_id_T0', 'movi_id_T1', 'movi_id_T2', 'movi_id_T3']]

        # After merging with female data save only concatenated file
        if cntr == 'SK_Female' or cntr == 'SK_Kosice_Female':
            pass  # do nothing
        else:
            result_df.to_excel(writer, cntr)

    # close the Excel writer at the end of the loop
    writer.close()

def add_center_name(df):
    # Try to get the center name with proper participant_id naming; if naming is not correct add participant_id_error string
    try:
        df['centerName'] = np.where(df['participant_id'].str.contains('I_BI_[A-Z]_\d{3}$|I-BI-[A-Z]-\d{3}$', regex=True) == True, 'BI',
            np.where(df['participant_id'].str.contains('I_LE_[A-Z]_\d{3}$|I-LE-[A-Z]-\d{3}$', regex=True) == True,'LE',
                np.where(df['participant_id'].str.contains('I_MA_[A-Z]_\d{3}$|I-MA-[A-Z]-\d{3}$', regex=True) == True, 'MA',
                         np.where(df['participant_id'].str.contains('I_WI_[A-Z]_\d{3}$|I-WI-[A-Z]-\d{3}$', regex=True) == True, 'WI',
                                  np.where(df['participant_id'].str.contains('I_LO_[A-Z]_\d{3}$|I-LO-[A-Z]-\d{3}$', regex=True) == True, 'LO',
                                      np.where(df['participant_id'].str.contains('I_CA_[A-Z]_\d{3}$|I-CA-[A-Z]-\d{3}$', regex=True) == True, 'CA',
                                               np.where(df['participant_id'].str.contains('I_BR_[A-Z]_\d{3}$|I-BR-[A-Z]-\d{3}$', regex=True) == True, 'BR',
                                                        np.where(df['participant_id'].str.contains('I_KO_[A-Z]_\d{3}$|I-KO-[A-Z]-\d{3}$', regex=True) == True,'KO',
                                                                 'participant_id_error'))))))))
    except:
        df['centerName'] = 'participant_id_error'
    return df

