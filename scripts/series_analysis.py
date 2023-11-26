import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats
import plotly.express as px
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
import plotly.graph_objects as go
from functions.preprocess import *
from statsmodels.tsa.arima_process import ArmaProcess

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
        tam = len(x)
        lista = np.array(list(range(1,tam+1)))
        X = np.column_stack(lista)
        X = X.reshape([tam,1])

        Xm = X ** np.arange(0,5)
        
        model = sm.OLS(y, Xm)
        results = model.fit()
        fitted_curve = results.predict(Xm)

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

    def stacionary_series(self, x, y):
        trend = self.series_trend(x, y)
        series_without_trend = y - trend
        stacionary_series = self.first_order_diff(series_without_trend)

        results = adfuller(stacionary_series)
        # fig = px.line(stacionary_series)

        return stacionary_series, results[1]

    def plot_autocorrelation(self, dataframe, beta_sample, plot_pacf=False, lags=None):
        dataframe = dataframe['Casos'] 
        corr_array = pacf(dataframe.dropna(), alpha=0.05, nlags=lags) if plot_pacf else acf(dataframe.dropna(), alpha=0.05, nlags=lags)
        lower_y = corr_array[1][:,0] - corr_array[0]
        upper_y = corr_array[1][:,1] - corr_array[0]

        # print(beta_sample)
        tam = 2
        # tam = 10 if beta_sample is not None else 2

        fig = go.Figure()
        [fig.add_scatter(x=(x,x), y=(0,corr_array[0][x]), mode='lines',line_color='#3f3f3f', line={'width': tam}) 
        for x in range(len(corr_array[0]))]
        fig.add_scatter(x=np.arange(len(corr_array[0])), y=corr_array[0], mode='markers', marker_color='#1f77b4',
                    marker_size=12)
        fig.add_scatter(x=np.arange(len(corr_array[0])), y=upper_y, mode='lines', line_color='rgba(255,255,255,0)')
        fig.add_scatter(x=np.arange(len(corr_array[0])), y=lower_y, mode='lines',fillcolor='rgba(32, 146, 230,0.3)',
                fill='tonexty', line_color='rgba(255,255,255,0)')
        
        # if beta_sample is not None:
        #     corr_array = pacf(beta_sample, alpha=0.05, nlags=lags) if plot_pacf else acf(beta_sample, alpha=0.05, nlags=lags)
        #     [fig.add_scatter(x=(x,x), y=(0,corr_array[0][x]), mode='lines',line_color='red') 
        #     for x in range(len(corr_array[0]))]



        fig.update_traces(showlegend=False)
        fig.update_xaxes(range=[-1,lags+1])
        fig.update_yaxes(zerolinecolor='#000000')
        
        title='Partial Autocorrelation (PACF)' if plot_pacf else 'Autocorrelation (ACF)'
        fig.update_layout(title=title)
        return fig
    

    def medias_moveis_betas(self, betas, nsample):
        ar1 = np.array([1])
        ma1 = np.array([1, *betas])
        model = ArmaProcess(ar1, ma1)
        sample = model.generate_sample(nsample=nsample)
        return sample