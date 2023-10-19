import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


class SeriesAnalysis:
    def plot_series(self, xaxis, yaxis, xlabel, ylabel, title, figsize=(15, 4)):
        f, ax = plt.subplots(figsize=figsize)
        ax.plot(xaxis, yaxis, color="tab:red")
        ax.set(title=title, xlabel=xlabel, ylabel=ylabel)

        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

        return ax

    def boxcox_transformation(self, xaxis, yaxis, xlabel, ylabel, title, lmbda):
        transformed_data = stats.boxcox(yaxis, lmbda=lmbda)
        return self.plot_series(xaxis, transformed_data, xlabel, ylabel, title)

    def series_trend(self, x, y):
        model = sm.OLS(y, x)
        results = model.fit()
        fitted_curve = results.predict(x)

        return fitted_curve

    def linear_filter(self, series, k):
        weights = np.ones(k) / k
        return pd.Series(np.convolve(series, weights, mode="valid"))

    def first_order_diff(self, series):
        return pd.Series(np.diff(series))

    def sazonal_diff(self, series, k):
        return pd.Series(series[k - 1 :] - series[: -(k - 1)])

    def autocorrelation(self, y, lags):
        return plot_acf(y.tolist(), lags=lags)

    def partial_autocorrelation(self, y, lags):
        return plot_pacf(y.tolist(), lags=lags)
