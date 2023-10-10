import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from assets.data import dataset
from assets.select_data import _select_data
from functions.sazonalidade import plot_seasonality
from functions.subseries import plot_subseries
from functions.preprocess import *

from scipy import stats
from scipy.optimize import curve_fit
import statsmodels.api as sm
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

import numpy as np

dash.register_page(__name__, name='Exploração', title='DATASUS | Exploração')

filtro_ano = ['Todos']
filtro_ano.extend(list(range(1996,2022)))

layout = dbc.Container([
    # Titulo
    dbc.Row([
        dbc.Col(html.H2(['Exploração dos dados']),
                style={'padding':20})
    ]),

    # Seleciona dados
    dbc.Row(_select_data),

    dbc.Row([
        # Grafico
        dbc.Col(
            dcc.Loading(
                    id='plot',
                    type='circle'
                ),
            width=9
        ),

        # Filtros
        dbc.Col([
            html.H4('Selecione os filtros',
                style={'padding':20}
            ),
            dcc.RadioItems(
                    ['Diario', 'Mensal', 'Anual'],
                    id='agrupamento',
                    persistence=True, 
                    persistence_type='session',
                    style={'padding':20},
                    inline=True,
                    value='Mensal',
                    inputStyle={'margin-left': "20px",
                                'margin-right':'3px'}
                    ),

            dcc.Dropdown(
                # filtro_ano,
                list(range(1996,2022)),
                id='anos',
                persistence=True, 
                persistence_type='session', 
                placeholder = 'Selecione um ano',
                multi=True,
                searchable=False
            ),
                    
            html.H4('Selecione o tipo de gráfico',
                style={'padding':20}
            ),
            
            dcc.Dropdown(
                ['Temporal','Sazonalidade','Sub-Séries','Multi-sazonalidade','Defasagens'],
                value='Temporal',
                id='plot_type',
                persistence=True,
                persistence_type='session', 
                placeholder = 'Tipo de gráfico',
                searchable=False
            )
        ]),
    ]),

    dbc.Row(dcc.RadioItems(
                    ['Nenhum', '1a Diferenciação', '2a Diferenciação', 'Box-Cox', 'Média Móvel', 'Tendência'],
                    value = 'Nenhum',
                    id='transformacoes',
                    persistence=True, 
                    persistence_type='session',
                    inline=True,
                    inputStyle={'margin-left': "20px",
                                'margin-right':'3px'}
                    )),
    dbc.Row(dcc.Input(
                id='box-cox',
                type='text',
                # value = 1,
                placeholder = 'Selecionar Lambda'
            ) )
])

@callback(
    Output(component_id='plot', component_property='children'),
    Input(component_id='bases', component_property='value'),
    Input(component_id='dataset', component_property='value'),
    Input(component_id='anos', component_property='value'),
    Input(component_id='agrupamento', component_property='value'),
    Input(component_id='plot_type', component_property='value'),
    Input(component_id='transformacoes', component_property='value'),
    Input(component_id='box-cox', component_property='value')
)
def data_plot(base_chosen, table, ano, agrupamento, plot_type, transformacao, lambda_box_cox):

    # Resolvendo bug tipo de dado
    if type(table) == list:
        df = dataset[base_chosen][table[0]]
    else:
        df = dataset[base_chosen][table]

    # Filtra os dados
    if ano != []:
        df_ano = df[df['DATA'].apply(lambda x: int(x[:4])).isin(ano)].copy()
    else:
        df_ano = df.copy()

    # Preprocessa os dados
    if base_chosen == 'SINAN':
        df_process = preprocess_SINAN(df_ano, agrupamento)
    elif base_chosen == 'SIM':
        df_process = preprocess_SIM(df_ano, agrupamento)    

    if transformacao != 'Nenhum':
        if transformacao == 'Box-Cox' and lambda_box_cox != None:
            df_process['Casos'] = stats.boxcox(df_process['Casos'], lmbda = int(lambda_box_cox))

        elif transformacao == 'Tendência':
            tam = len(df_process['Casos'])
            lista = np.array(list(range(1,tam+1)))
            X = np.column_stack(lista)
            X = X.reshape([tam,1])

            Xm = X ** np.arange(0,5)

            model = sm.OLS(df_process['Casos'],Xm)
            results = model.fit()

            df_process['Casos'] = df_process['Casos']-results.predict(Xm)

    # Cria figura
    if plot_type == 'Sazonalidade':
        return dcc.Graph(figure = plot_seasonality(df_process,'Data','Casos','b', 'Y', title='Gráfico de Sazonalidade'))
    
    elif plot_type == 'Temporal':
        return dcc.Graph(figure = px.line(data_frame=df_process, x='Data', y='Casos', title=f'Gráfico por tempo'))
    
    elif plot_type == 'Sub-Séries':
        return dcc.Graph(figure = plot_subseries(df_process,'Data','Casos',title='Gráfico de Sub-Séries'))