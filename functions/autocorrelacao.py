from statsmodels.tsa.stattools import acf, pacf
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from functions.preprocess import *

def plot_autocorrelation(dataframe, agrupamento_autocorr, plot_pacf=False, lags=None):
    
    df_agrupado = preprocess_SIM(dataframe, agrupamento_autocorr)
    df_agrupado = df_agrupado['Casos'] 
    corr_array = pacf(df_agrupado.dropna(), alpha=0.05, nlags=lags) if plot_pacf else acf(df_agrupado.dropna(), alpha=0.05, nlags=lags)
    lower_y = corr_array[1][:,0] - corr_array[0]
    upper_y = corr_array[1][:,1] - corr_array[0]

    fig = go.Figure()
    [fig.add_scatter(x=(x,x), y=(0,corr_array[0][x]), mode='lines',line_color='#3f3f3f') 
     for x in range(len(corr_array[0]))]
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=corr_array[0], mode='markers', marker_color='#1f77b4',
                   marker_size=12)
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=upper_y, mode='lines', line_color='rgba(255,255,255,0)')
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=lower_y, mode='lines',fillcolor='rgba(32, 146, 230,0.3)',
            fill='tonexty', line_color='rgba(255,255,255,0)')
    fig.update_traces(showlegend=False)
    fig.update_xaxes(range=[-1,lags+1])
    fig.update_yaxes(zerolinecolor='#000000')
    
    title='Partial Autocorrelation (PACF)' if plot_pacf else 'Autocorrelation (ACF)'
    fig.update_layout(title=title)
    return fig