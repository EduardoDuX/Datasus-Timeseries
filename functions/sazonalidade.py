import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PERIODS = {
    "Y": 'Ano',
    "b": 'Mês',
    "d": 'Dia',
    "H": "Hora",
    "M": "Minuto",
}

MONTHS = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

def format_dates(dataframe, date_column, period, default_period):
    """
    Formats dates in a DataFrame according to the specified period.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing the data.
        date_column (str): The name of the date column.
        period (str): The desired formatting period (e.g., "Y" for year, "b" for month).
        default_period (str): The default format to be used if the period is not recognized.

    Returns:
        pd.Series: A series with the formatted dates.
    """
    dataframe[date_column] = pd.to_datetime(dataframe[date_column])
    periodo_mapping = {"Y": "%Y", "b": "%b", "d": "%d", "H": "%H", "M": "%M"}
    return dataframe[date_column].dt.strftime(periodo_mapping.get(period, default_period))

def plot_seasonality(dataframe, date_column, value_column, grouping_period, observation_period, title=""):
    """
    Creates a seasonal plot from a DataFrame.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing the data.
        date_column (str): The name of the date column.
        value_column (str): The name of the column with the values to be plotted.
        grouping_period (str): The grouping period (e.g., "Y" for year, "b" for month).
        observation_period (str): The observation period (e.g., "Y" for year, "b" for month).
        title (str): The title of the plot.

    """
    df = dataframe.copy()
    grouping_period_label = PERIODS.get(grouping_period, "%b")
    observation_period_label = PERIODS.get(observation_period, "%Y")

    df[grouping_period_label] = format_dates(df, date_column, grouping_period, '%b')
    df[observation_period_label] = format_dates(df, date_column, observation_period, '%Y')

    palette = sns.color_palette("Set2", len(df[observation_period_label].unique()))
    g = sns.relplot(data=df, x=grouping_period_label, y=value_column, hue=observation_period_label, kind="line", palette=palette, height=5.5)

    plt.title(title, fontweight='bold', fontsize=14)
    plt.ylabel(value_column)

    # Configure x-axis ticks (if it's monthly)
    if grouping_period == "b":
        plt.xticks(range(12), MONTHS)

    sns.set(style='darkgrid')
    plt.grid(True, alpha=0.6)
    plt.show()