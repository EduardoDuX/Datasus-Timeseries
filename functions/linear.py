import pandas as pd
from functions.preprocess import *
import numpy as np
from scipy import stats
import statsmodels.api as sm
import plotly.express as px
import plotly.graph_objects as go
from scripts.series_analysis import SeriesAnalysis

series_analysis = SeriesAnalysis()

def linear(df, base_chosen, ano, agrupamento, transformacao, lambda_box_cox, plot_pacf=False, lags=None):
    if ano != [] and ano != None:
        df_ano = df[df['DATA'].apply(lambda x: int(x[:4])).isin(ano)].copy()
    else:
        df_ano = df.copy()
    # Preprocessa os dados
    df_process = preprocess(df_ano, agrupamento)

    if transformacao != 'Nenhum':
        
        if transformacao == 'Box-Cox' and lambda_box_cox != None:
            df_process['Casos'] = stats.boxcox(df_process['Casos'], lmbda = float(lambda_box_cox))

        elif transformacao == 'Tendência':
            fitted_curve = series_analysis.series_trend(df_process[agrupamento], df_process['Casos'])
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_process[agrupamento], y=fitted_curve, mode='lines', name='Tendência'))
            fig.add_trace(go.Scatter(x=df_process[agrupamento], y=df_process['Casos'], mode='lines', name='Série'))
            return fig

        elif transformacao == '1a Diferenciação':
            df_process['Casos'] = pd.Series(np.diff(df_process['Casos']))

        elif transformacao == '2a Diferenciação':
            df_process['Casos'] = pd.Series(np.diff(np.diff(df_process['Casos'])))

        elif transformacao == 'Média Móvel':
            k = int(lambda_box_cox)
            weights = np.ones(k) / k
                        
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_process[agrupamento], y=pd.Series(np.convolve(df_process['Casos'], weights, mode="valid")), mode='lines', name='Média Móvel'))
            fig.add_trace(go.Scatter(x=df_process[agrupamento], y=df_process['Casos'], mode='lines', name='Série'))
            return fig
            
            
        elif transformacao == 'Estacionariedade':
            x, p_value = series_analysis.stacionary_series(df_process[agrupamento], df_process['Casos'])
            df_process['Casos'] = x
            
        elif transformacao == 'Autocorrelação':
            fig, _ = series_analysis.plot_autocorrelation(df_process, None, plot_pacf, lags)
            return fig
                
                
    return px.line(data_frame=df_process, x=agrupamento, y='Casos', title=f'Gráfico por tempo')