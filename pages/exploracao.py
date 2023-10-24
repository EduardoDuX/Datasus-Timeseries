import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from assets.data import dataset
from assets.select_data import _select_data
from functions.sazonalidade import plot_seasonality
from functions.subseries import plot_subseries
from functions.autocorrelacao import plot_autocorrelation

from functions.preprocess import *
from functions.linear import linear

from assets.FiltrosExplorar.FiltroTemporal import _temporal
from assets.FiltrosExplorar.FiltroSazonalidade import _sazonalidade
from assets.FiltrosExplorar.FiltroAutocorrelacao import _autocorr

from scipy import stats
from scipy.optimize import curve_fit
import statsmodels.api as sm
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

import numpy as np
import time

dash.register_page(__name__, name='Exploração', title='DATASUS | Exploração')

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
            _select_data, width = 7, style={'border-right': '1px solid black'}
        ),   
        
        # Seleciona tipo de gráfico
        dbc.Col([
            dbc.Row(
                html.H4('Selecione o tipo de gráfico',
                    style={'padding':10, 'text-align': 'center'}
                )
            ),
            
            dbc.Row(
                dcc.Dropdown(
                    ['Temporal','Sazonalidade', 'Auto-Correlação','Sub-Séries','Multi-sazonalidade','Defasagens'],
                    value='Temporal',
                    id='plot_type',
                    persistence=True,
                    persistence_type='session', 
                    placeholder = 'Tipo de gráfico',
                    style={'margin-bottom': '5  px', 'text-align': 'center'},
                    searchable=False
                )
            )
        ], width = 4)
    ],style={'background-color':'#BDC3C7', 'border-radius': '10px'}),
    
    # Filtros e gráfico 

    dbc.Row([
        # Grafico
        dbc.Col(
                id='filters',
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
            id='plot',
            type='circle'
        ),
        style={'margin-top': '30px', 'margin-bottom': '50px'}
    )
])

@callback(
    Output(component_id='filters', component_property='children'),
    Input(component_id='plot_type', component_property='value')
)
def filters_function(plot_type):
    child = None
    if plot_type == 'Temporal':
        child =  _temporal
    elif plot_type == 'Sazonalidade':
        child =  _sazonalidade
    elif plot_type == 'Auto-Correlação':
        child = _autocorr
    return child

@callback(
    Output(component_id='plot', component_property='children'),
    Input(component_id='graph_gen', component_property='n_clicks_timestamp'),
    Input(component_id='bases', component_property='value'),
    Input(component_id='dataset', component_property='value'),
    Input(component_id='plot_type', component_property='value'),
    Input(component_id='agrupamento_linear', component_property='value'),
    Input(component_id='anos_linear', component_property='value'),
    Input(component_id='transformacoes_linear', component_property='value'),
    Input(component_id='box-cox_linear', component_property='value'),
    Input(component_id='eixo_sazonalidade', component_property='value'),
    Input(component_id='agrupamento_sazonalidade', component_property='value'),
    Input(component_id='agrupamento_autocorr', component_property='value'),
    Input(component_id='lags_autocorr', component_property='value'),
    Input(component_id='pacf_autocorr', component_property='value')

)
def data_plot(timestamp, base_chosen, sub_base, plot_type, agrupamento_linear = None, ano_linear = None, transformacao_linear = None, lambda_box_cox_linear = None, eixo_sazonalidade = None, agrupamento_sazonalidade = None, agrupamento_autocorr = None, lags_autocorr = None, par_pacf = None):
    
    sis = str(time.time_ns())[:11] 
    # Resolvendo bug tipo de dado
    if type(sub_base) == list:
        df = dataset[base_chosen][sub_base[0]]
    else:
        df = dataset[base_chosen][sub_base]

    df = df.loc[df['DATA'].apply(lambda x: len(str(x))) > 8]    

    if timestamp != None and sis == str(timestamp+10)[:11]:
        # Cria figura
        if plot_type == 'Sazonalidade':
            if  eixo_sazonalidade == agrupamento_sazonalidade:
                return html.H4('Eixo e Agrupamento não podem ser iguais')
            return dcc.Graph(figure = plot_seasonality(df,eixo_sazonalidade, agrupamento_sazonalidade))
        
        elif plot_type == 'Temporal':
            return dcc.Graph(figure = linear(df, base_chosen, ano_linear, agrupamento_linear, transformacao_linear, lambda_box_cox_linear))
        
        elif plot_type == 'Sub-Séries':
            pass

        elif plot_type == 'Multi-sazonalidade':
            pass

        elif plot_type == 'Defasagens':
            pass
        
        elif plot_type == 'Auto-Correlação':
            convert = {'PACF': True,'ACF': False}
            return dcc.Graph(figure = plot_autocorrelation(df, agrupamento_autocorr, convert[par_pacf], int(lags_autocorr)))


@callback(
    Output(component_id='box-cox_linear', component_property='disabled'),
    Input(component_id='transformacoes_linear', component_property='value')
)
def input_activation(transformacao):
    if transformacao == 'Box-Cox' or transformacao == 'Média Móvel':
        return False
    else:
        return True