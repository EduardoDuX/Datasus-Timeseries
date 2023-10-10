import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd

def plot_subseries(dataframe, date_column, value_column, title="Month Plot"):
    """
    Create subplots for a time series DataFrame with monthly highlights.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing the time series data.
        date_column (str): The name of the date column.
        value_column (str): The name of the column with the time series values.
        title (str): The title of the subplots.
    """
    # Ensure the DataFrame is sorted by date
    dataframe = dataframe.sort_values(by=date_column)

    # Convert the date column to datetime and set it as the index
    dataframe[date_column] = pd.to_datetime(dataframe[date_column])
    dataframe.set_index(date_column, inplace=True)

    # Resample data to monthly frequency using mean
    if dataframe.index.freq != 'M':
        dataframe = dataframe.resample('M').mean()

    # Create the time series
    ts = dataframe[value_column]

    # Create subplots for each month
    sm.graphics.tsa.month_plot(ts)
    plt.title(title, fontweight='bold', fontsize=14)
    print(ts)
    print(type(ts))
    plt.show()