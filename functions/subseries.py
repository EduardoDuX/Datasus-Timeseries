import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd

def plot_subseries(dataframe, date_column, value_column):
    """
    Create subplots for a time series DataFrame with monthly highlights.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing the time series data.
        date_column (str): The name of the date column.
        value_column (str): The name of the column with the time series values.
        title (str): The title of the subplots.
    """

    # Resample data to monthly frequency using mean
    if dataframe.index.freq != 'M':
        dataframe = dataframe.resample('M').mean()

    # Create the time series
    ts = dataframe[value_column]

    # Create subplots for each month
    sm.graphics.tsa.month_plot(ts)
    print(ts)
    print(type(ts))
    plt.show()