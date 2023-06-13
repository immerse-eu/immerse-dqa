# Required Libraries
import matplotlib as matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as backend_pdf


# function to create and save dashboard figures
def prepareFigures(config, dfDashboard):
    # Export dashboard as PDF file
    pdf = backend_pdf.PdfPages(config["localPaths"]["basePathDqa"] + "/ecrf_status_dashboard.pdf")

    # loop to create aggregated status plots for every ecrf_acronym
    for acronym in dfDashboard.ecrf_acronym.unique():
        # make a copy of the original dfDashboard object
        df = dfDashboard.copy()
        # create binary values for ecrf_status
        binary_status = pd.get_dummies(df.ecrf_status)
        # add binary values to dataframe
        df2 = pd.concat([df, binary_status], axis=1)
        # group dataframe by center_name and aggregate the sum of the ecrf_status for each center_name
        df3 = df2[df2.ecrf_acronym == acronym].groupby('center_name').aggregate(["sum"])
        # reformat dataframe for sns plotting
        df_plot = pd.concat([df3.COMPLETED, df3.STARTED, df3.EMPTY], axis=1)
        df_plot.columns = ["COMPLETED", "STARTED", "EMPTY"]
        df_plot2 = pd.concat([df3.COMPLETED, df3.STARTED, df3.EMPTY], axis=0)
        df_plot2 = pd.DataFrame(df_plot2)
        df_plot2["status"] = ['COMPLETE'] * len(df_plot.COMPLETED) + ['STARTED'] * len(df_plot.COMPLETED) + ['EMPTY'] * len(df_plot.COMPLETED)
        df_plot2["center_name"] = df_plot2.index
        df_plot2.columns = ["status_accumulation", "status", "center_name"]

        # create bar plot
        bar_plot = sns.barplot(data=df_plot2, x="center_name", y="status_accumulation", hue="status", color = 'green', palette = ['tab:green', 'tab:orange', 'tab:red'])
        # add title to every plot
        bar_plot.set(title='eCRF: ' + acronym)
        # get specific sns figure for saving and save each figure in loop into pdf object
        pdf.savefig(bar_plot.get_figure())
        # close the sns plot
        plt.close(bar_plot.get_figure())
    # finally close pdf object to save pdf
    pdf.close()