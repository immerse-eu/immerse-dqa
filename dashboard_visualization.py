# Required Libraries
import matplotlib as matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as backend_pdf


# function to create and save dashboard figures
def prepareFigures(config, dfDashboard):
    ### accumulated status for all centers with separated plots for each eCRF
    # Export dashboard as PDF file
    pdf_ecrf = backend_pdf.PdfPages(config["localPaths"]["basePathDqa"] + "/ecrf_center_status_dashboard.pdf")
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
        df_ecrf_3 = df_ecrf_2[df_ecrf_2.ecrf_acronym == acronym].groupby('center_name').aggregate(["sum"])
        # reformat dataframe for sns plotting
        df_ecrf_plot = pd.concat([df_ecrf_3.COMPLETED, df_ecrf_3.STARTED, df_ecrf_3.EMPTY], axis=1)
        df_ecrf_plot.columns = ["COMPLETED", "STARTED", "EMPTY"]
        df_ecrf_plot2 = pd.DataFrame(df_ecrf_plot)
        df_ecrf_plot2["center_name"] = df_ecrf_plot.index
        # create bar plot
        bar_plot_ecrf = df_ecrf_plot2.set_index('center_name').plot(kind='bar', stacked=True, color=['green', 'orange', 'red'])
        # add title to every plot
        bar_plot_ecrf.set(title='eCRF: ' + acronym,  xlabel ="center_name", ylabel = "status_accumlation")
        # get specific sns figure for saving and save each figure in loop into pdf object
        pdf_ecrf.savefig(bar_plot_ecrf.get_figure(), dpi=300, bbox_inches='tight')
        # close the sns plot
        plt.close(bar_plot_ecrf.get_figure())
    # finally close pdf object to save pdf
    pdf_ecrf.close()


    ### accumulated status for all visit_names with separated plots for each center
    # Export dashboard as PDF file
    pdf_center = backend_pdf.PdfPages(config["localPaths"]["basePathDqa"] + "/center_visit_status_dashboard.pdf")
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
        df_center_plot = pd.concat([df_center_3.COMPLETED, df_center_3.STARTED, df_center_3.EMPTY], axis=1)
        df_center_plot.columns = ["COMPLETED", "STARTED", "EMPTY"]
        df_center_plot2 = pd.DataFrame(df_center_plot)
        df_center_plot2["visit_name"] = df_center_plot.index
        # create bar plot
        bar_plot_center = df_center_plot2.set_index('visit_name').plot(kind='bar', stacked=True, color=['green', 'orange', 'red'])
        # add title to every plot
        bar_plot_center.set(title='Center Name: ' + center, xlabel ="visit_name", ylabel = "status_accumlation")
        # get specific sns figure for saving and save each figure in loop into pdf object
        pdf_center.savefig(bar_plot_center.get_figure(), dpi=300, bbox_inches='tight')
        # close the sns plot
        plt.close(bar_plot_center.get_figure())
    # finally close pdf object to save pdf
    pdf_center.close()
