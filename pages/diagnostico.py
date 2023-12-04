import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from assets.data import dataset
from assets.select_data import _select_data
from assets.FiltrosExplorar.FiltroDiagnostico import _diag
from scripts.series_analysis import SeriesAnalysis
from statsmodels.tsa.arima.model import ARIMA
import time
from functions.preprocess import *
from statsmodels.graphics.api import qqplot
import numpy as np

dash.register_page(__name__, name='Diagnóstico', title='DATASUS | Diagnóstico')

filtro_ano = ['Todos']
filtro_ano.extend(list(range(1996,2022)))

n_global = 0

layout = dbc.Container([
    # Titulo
    dbc.Row([
        dbc.Col(html.H2(['Diagnóstico de modelos']),
                style={'padding':20})
    ]),

    # Seleciona dados
    dbc.Row([

        # Seleciona Base
        dbc.Col(
            _select_data
        ),   
        
    ],style={'background-color':'#BDC3C7', 'border-radius': '10px'}),
    
    # Filtros e gráfico 

    dbc.Row([
        # Grafico
        dbc.Col(
                _diag,
            )
        ], style={'background-color':'#C2C8CC', 'border-top-left-radius': '10px','border-top-right-radius': '10px', 'margin-top': '15px','border-bottom': '1px solid black'}),

        dbc.Row([
            dbc.Row(
                html.H4('Gerar Gráfico (série estacionária)',
                style={'padding':15, 'text-align': 'center'})
            ),

            dbc.Row(
                dbc.Button("Confirma", color="secondary", id="graph_gen", value = 'Click', style={'padding':10}),
                style={'padding':15}
            )
        ], justify = 'center',
        style={'background-color':'#C2C8CC', 'border-bottom-left-radius': '10px','border-bottom-right-radius': '10px'}),
    

    dbc.Row(
        # Grafico
        dcc.Loading(
            id='plot_diag',
            type='circle'
        ),
        style={'margin-top': '30px', 'margin-bottom': '50px'}
    ),
    dbc.Row(
        # Análise
        dcc.Loading(
            id='analisys_model',
            type='circle'
        ),
        style={'margin-top': '30px', 'margin-bottom': '50px'}
    )
])

@callback(
    Output(component_id='plot_diag', component_property='children'),
    Input(component_id='graph_gen', component_property='n_clicks_timestamp'),
    Input(component_id='bases', component_property='value'),
    Input(component_id='dataset', component_property='value'),
    Input(component_id='agrupamento_diag', component_property='value'),
    Input(component_id='q', component_property='value'),
    Input(component_id='p', component_property='value')
)
def diagnostico(timestamp, base_chosen, sub_base, agrupamento, q, p):
    # print(transformacoes)
    sis = str(time.time_ns())[:11] 
    if timestamp != None and sis == str(timestamp+10)[:11]:
        q = int(q)
        p = int(p)


        df = dataset[base_chosen][sub_base]
        df = preprocess(df, agrupamento)

        series_analysis = SeriesAnalysis()
        df['Casos'], _ = series_analysis.stacionary_series(df[agrupamento], df['Casos'])
        df = df[['Casos',agrupamento]]
        df.index.freq = df[agrupamento]
        del df[agrupamento]
        arma_mod = ARIMA(df, order=(p, 0, q)).fit()
        resid = arma_mod.resid

        qqplot_data = qqplot(resid, line='q').gca().lines

        fig = go.Figure()

        fig.add_trace({
            'type': 'scatter',
            'x': qqplot_data[0].get_xdata(),
            'y': qqplot_data[0].get_ydata(),
            'mode': 'markers',
            'marker': {
                'color': '#1f77b4'
            }
        })

        fig.add_trace({
            'type': 'scatter',
            'x': qqplot_data[1].get_xdata(),
            'y': qqplot_data[1].get_ydata(),
            'mode': 'lines',
            'line': {
                'color': 'red'
            }

        })


        fig['layout'].update({
            'title': 'Gráfico de resíduos',
            'xaxis': {
                'title': 'Quantis Teóricos',
                'zeroline': False
            },
            'yaxis': {
                'title': 'Quantis da amostra'
            },
            'showlegend': False
        })

        return dcc.Graph(figure = fig)