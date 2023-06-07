# Required Libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# function to create and save dashboard figures
def prepareFigures(config, dfDashboard):
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
        df_plot2.columns = ["data", "status", "center_name"]

        # Uncomment for testing visualization in IDE
        # f, ax = plt.subplots()
        # sns.barplot(data=df_plot2, x="center_name", y="data", hue="status", ax=ax, color='green', palette=['tab:green', 'tab:orange', 'tab:red'])

        # create bar plot
        bar_plot = sns.barplot(data=df_plot2, x="center_name", y="data", hue="status", color = 'green', palette = ['tab:green', 'tab:orange', 'tab:red'])
        # get specific sns figure for saving
        fig = bar_plot.get_figure()
        # Export dashboard as PDF file
        fig.savefig(config["localPaths"]["basePathDqa"] + "/" + acronym + ".pdf")
        # close the sns plot
        plt.close(fig)
