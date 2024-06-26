# Required Libraries
import matplotlib as matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as backend_pdf
import os
from datetime import datetime

# Preparation for file naming
today = datetime.today()
created_date = today.strftime('%Y-%m-%d')

# function to create and save dashboard figures
def prepareFigures(config, dfDashboard):
    # set folder paths
    basePath_Dqa = config["localPaths"]["basePathDqa"]
    validation_csv_folder = config["localPaths"]["basePathDqa"] + "/validation_csv"

    # create_folders if not existing
    if not os.path.exists(basePath_Dqa):
        os.makedirs(basePath_Dqa)
    if not os.path.exists(validation_csv_folder):
        os.makedirs(validation_csv_folder)


    ### accumulated status for all centers with separated plots for each eCRF
    # Export dashboard as PDF file
    pdf_ecrf = backend_pdf.PdfPages(basePath_Dqa + "/ecrf_center_status_dashboard_createdOn_" + created_date + ".pdf")
    # make a copy of the original dfDashboard object
    df_ecrf = dfDashboard.copy()
    # remove main center name from the df
    df_ecrf = df_ecrf[df_ecrf.center_name != "main"]
    # remove all participants not included in the study
    df_ecrf = df_ecrf[df_ecrf.included_in_study == "included"]

    # loop to create aggregated status plots for every ecrf_acronym
    for acronym in df_ecrf.ecrf_acronym.unique():
        # create binary values for ecrf_status
        binary_status_ecrf = pd.get_dummies(df_ecrf.ecrf_status)
        # add binary values to dataframe
        df_ecrf_2 = pd.concat([df_ecrf, binary_status_ecrf], axis=1)
        # group dataframe by center_name and aggregate the sum of the ecrf_status for each center_name
        if acronym not in ["DIAGNOSIS", "CSRI_BE", "BEAQ"]:
            df_ecrf_3 = df_ecrf_2[df_ecrf_2.ecrf_acronym == acronym].groupby('center_name').aggregate(["sum"])

        elif acronym == "DIAGNOSIS":
            # ----- for "Baseline (clinician)" of "DIAGNOSIS" ----------
            df_ecrf_3a =  df_ecrf_2[(df_ecrf_2.ecrf_acronym == "DIAGNOSIS") & (df_ecrf_2.visit_name == "Baseline (clinician)")].groupby('center_name').aggregate(["sum"])
            # reformat dataframe for sns plotting
            df_ecrf_plot = pd.concat(
                [df_ecrf_3a.COMPLETED, df_ecrf_3a.quickCOMPLETED, df_ecrf_3a.STARTED, df_ecrf_3a.EMPTY], axis=1)
            df_ecrf_plot.columns = ["COMPLETED", "quickCOMPLETED", "STARTED", "EMPTY"]
            df_ecrf_plot2 = pd.DataFrame(df_ecrf_plot)
            df_ecrf_plot2["center_name"] = df_ecrf_plot.index
            # create bar plot
            bar_plot_ecrf = df_ecrf_plot2.set_index('center_name').plot(kind='bar', stacked=True,
                                                                        color=['green', 'yellowgreen', 'orange', 'red'])
            # add numbers to the bar plot
            for container in bar_plot_ecrf.containers:
                bar_label_ecrf = bar_plot_ecrf.bar_label(container, fmt='%d', label_type='center')
                for label in bar_label_ecrf:
                    if label.get_text() == '0':
                        label.set_text('')
            # add title to every plot
            bar_plot_ecrf.set(title='eCRF: ' + acronym + ' *only Baseline (clinician)', xlabel="center_name",
                                  ylabel="status_accumlation")

            # get specific sns figure for saving and save each figure in loop into pdf object
            pdf_ecrf.savefig(bar_plot_ecrf.get_figure(), dpi=300, bbox_inches='tight')
            # close the sns plot
            plt.close(bar_plot_ecrf.get_figure())


            # ----- for "Screening" of "DIAGNOSIS" ----------
            df_ecrf_3b =  df_ecrf_2[(df_ecrf_2.ecrf_acronym == "DIAGNOSIS") & (df_ecrf_2.visit_name == "Screening")].groupby('center_name').aggregate(["sum"])
            # reformat dataframe for sns plotting
            df_ecrf_plot = pd.concat(
                [df_ecrf_3b.COMPLETED, df_ecrf_3b.quickCOMPLETED, df_ecrf_3b.STARTED, df_ecrf_3b.EMPTY], axis=1)
            df_ecrf_plot.columns = ["COMPLETED", "quickCOMPLETED", "STARTED", "EMPTY"]
            df_ecrf_plot2 = pd.DataFrame(df_ecrf_plot)
            df_ecrf_plot2["center_name"] = df_ecrf_plot.index
            # create bar plot
            bar_plot_ecrf = df_ecrf_plot2.set_index('center_name').plot(kind='bar', stacked=True,
                                                                        color=['green', 'yellowgreen', 'orange', 'red'])
            # add numbers to the bar plot
            for container in bar_plot_ecrf.containers:
                bar_label_ecrf = bar_plot_ecrf.bar_label(container, fmt='%d', label_type='center')
                for label in bar_label_ecrf:
                    if label.get_text() == '0':
                        label.set_text('')
            # add title to every plot
            bar_plot_ecrf.set(title='eCRF: ' + acronym + ' *only Screening', xlabel="center_name",
                              ylabel="status_accumlation")

            # get specific sns figure for saving and save each figure in loop into pdf object
            pdf_ecrf.savefig(bar_plot_ecrf.get_figure(), dpi=300, bbox_inches='tight')
            # close the sns plot
            plt.close(bar_plot_ecrf.get_figure())

        elif acronym == "CSRI_BE":
            df_ecrf_3 = df_ecrf_2[(df_ecrf_2.ecrf_acronym == "CSRI_BE") & (df_ecrf_2.visit_name == "Baseline (patient)")].groupby('center_name').aggregate(["sum"])

        elif acronym == "BEAQ":
            df_ecrf_3 = df_ecrf_2[(df_ecrf_2.ecrf_acronym == "BEAQ") & (df_ecrf_2.visit_name == "Enrolment (patient)")].groupby('center_name').aggregate(["sum"])

        # reformat dataframe for sns plotting
        if not acronym == "DIAGNOSIS":
            df_ecrf_plot = pd.concat([df_ecrf_3.COMPLETED, df_ecrf_3.quickCOMPLETED, df_ecrf_3.STARTED, df_ecrf_3.EMPTY], axis=1)
            df_ecrf_plot.columns = ["COMPLETED", "quickCOMPLETED", "STARTED", "EMPTY"]
            df_ecrf_plot2 = pd.DataFrame(df_ecrf_plot)
            df_ecrf_plot2["center_name"] = df_ecrf_plot.index
            # create bar plot
            bar_plot_ecrf = df_ecrf_plot2.set_index('center_name').plot(kind='bar', stacked=True, color=['green', 'yellowgreen', 'orange', 'red'])
            # add numbers to the bar plot
            for container in bar_plot_ecrf.containers:
                bar_label_ecrf = bar_plot_ecrf.bar_label(container, fmt='%d', label_type='center')
                for label in bar_label_ecrf:
                    if label.get_text() == '0':
                        label.set_text('')
            # add title to every plot
            if acronym not in ["DIAGNOSIS", "CSRI_BE", "BEAQ"]:
                bar_plot_ecrf.set(title='eCRF: ' + acronym,  xlabel ="center_name", ylabel = "status_accumlation")
            elif acronym == "CSRI_BE":
                bar_plot_ecrf.set(title='eCRF: ' + acronym + ' *only Baseline(patient)', xlabel="center_name", ylabel="status_accumlation")
            elif acronym == "BEAQ":
                bar_plot_ecrf.set(title='eCRF: ' + acronym + ' *only Enrolment (patient)', xlabel="center_name", ylabel="status_accumlation")
            # get specific sns figure for saving and save each figure in loop into pdf object
            pdf_ecrf.savefig(bar_plot_ecrf.get_figure(), dpi=300, bbox_inches='tight')
            # close the sns plot
            plt.close(bar_plot_ecrf.get_figure())
            df_ecrf_plot2.to_csv(validation_csv_folder + "/" + acronym + "_center_status_dashboard.csv",
                                   sep=";", index=False)

    # finally close pdf object to save pdf
    pdf_ecrf.close()


    ### accumulated status for all visit_names with separated plots for each center
    # Export dashboard as PDF file
    pdf_center = backend_pdf.PdfPages(basePath_Dqa + "/center_visit_status_dashboard_createdOn_" + created_date + ".pdf")
    # make a copy of the original dfDashboard object
    df_center = dfDashboard.copy()
    # remove main center name from the df
    df_center = df_center[df_center.center_name != "main"]
    # remove all participants not included in the study
    df_center = df_center[df_center.included_in_study == "included"]

    # loop to create aggregated status plots for every ecrf_acronym
    for center in df_center.center_name.unique():
        # create binary values for ecrf_status
        binary_status_center = pd.get_dummies(df_center.ecrf_status)
        # add binary values to dataframe
        df_center_2 = pd.concat([df_center, binary_status_center], axis=1)
        # group dataframe by center_name and aggregate the sum of the ecrf_status for each center_name
        df_center_3 = df_center_2[df_center_2.center_name == center].groupby('visit_name').aggregate(["sum"])
        # reformat dataframe for sns plotting
        df_center_plot = pd.concat([df_center_3.COMPLETED, df_ecrf_3.quickCOMPLETED, df_center_3.STARTED, df_center_3.EMPTY], axis=1)
        df_center_plot.columns = ["COMPLETED", "quickCOMPLETED", "STARTED", "EMPTY"]
        df_center_plot2 = pd.DataFrame(df_center_plot)
        df_center_plot2["visit_name"] = df_center_plot.index
        # create bar plot
        bar_plot_center = df_center_plot2.set_index('visit_name').plot(kind='bar', stacked=True, color=['green', 'yellowgreen', 'orange', 'red'])
        # add numbers to the bar plot
        for container in bar_plot_center.containers:
            bar_label_center = bar_plot_center.bar_label(container, fmt='%d', label_type='center')
            for label in bar_label_center:
                if label.get_text() == '0':
                    label.set_text('')
        # add title to every plot
        bar_plot_center.set(title='Center Name: ' + center, xlabel ="visit_name", ylabel = "status_accumlation")
        # get specific sns figure for saving and save each figure in loop into pdf object
        pdf_center.savefig(bar_plot_center.get_figure(), dpi=300, bbox_inches='tight')
        # close the sns plot
        plt.close(bar_plot_center.get_figure())
        #df_center_plot2.to_csv(validation_csv_folder + center + "_visit_status_dashboard.csv", sep=";", index=False)
    # finally close pdf object to save pdf
    pdf_center.close()

def responsePerParticipants(config, responseInfo_all, created_date):
    # make a copy of the original dfDashboard object
    dfRsponseTable = responseInfo_all.copy()
    # remove main center name from the df
    dfRsponseTable = dfRsponseTable[dfRsponseTable.center_name != "main"]
    # save dataframe in xlsx & csv file
    dfRsponseTable.to_excel(
        config["localPaths"]["basePathDqa"] + "/maganamed_responseTableXLSX_createdOn_" + created_date + ".xlsx",
        index=False)
    dfRsponseTable.to_csv(
        config["localPaths"]["basePathDqa"] + "/maganamed_responseTableCSV_createdOn_" + created_date + ".csv", sep=";",
        index=False)
    return(dfRsponseTable)
