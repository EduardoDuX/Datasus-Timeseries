import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from assets.data import dataset
from assets.select_data import _select_data
from assets.FiltrosExplorar.FiltroAutocorrelacao import _autocorr
from scripts.series_analysis import SeriesAnalysis
import time
from functions.preprocess import *
import numpy as np

dash.register_page(__name__, name='Modelagem', title='DATASUS | Modelagem')


filtro_ano = ['Todos']
filtro_ano.extend(list(range(1996,2022)))

n_global = 0

layout = dbc.Container([
    # Titulo
    dbc.Row([
        dbc.Col(html.H2(['Exploração dos dados']),
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
                _autocorr,
            )
        ], style={'background-color':'#C2C8CC', 'border-top-left-radius': '10px','border-top-right-radius': '10px', 'margin-top': '15px','border-bottom': '1px solid black'}),

        dbc.Row([
            dbc.Row(
                html.H4('Gerar Gráfico',
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
            id='plot_model',
            type='circle'
        ),
        style={'margin-top': '30px', 'margin-bottom': '50px'}
    )
])

@callback(
    Output(component_id='plot_model', component_property='children'),
    Input(component_id='graph_gen', component_property='n_clicks_timestamp'),
    Input(component_id='bases', component_property='value'),
    Input(component_id='dataset', component_property='value'),
    Input(component_id='agrupamento_autocorr', component_property='value'),
    Input(component_id='lags_autocorr', component_property='value'),
    Input(component_id='pacf_autocorr', component_property='value')
)

def medias_moveis(timestamp, base_chosen, sub_base, agrupamento, lags, pacf):
    # print(transformacoes)
    sis = str(time.time_ns())[:11] 
    if timestamp != None and sis == str(timestamp+10)[:11]:
        lags = int(lags)
        # sample = None

        df = dataset[base_chosen][sub_base]
        df = preprocess(df, agrupamento)

        series_analysis = SeriesAnalysis()
        convert = {'PACF': True,'ACF': False, None: None}
        pacf = convert[pacf]
        
        df['Casos'], pvalor = series_analysis.stacionary_series(df[agrupamento], df['Casos'])
        print(pvalor)
        im = series_analysis.plot_autocorrelation(df, None, pacf, lags)
        return dcc.Graph(figure = im)