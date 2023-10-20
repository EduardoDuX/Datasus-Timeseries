import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from assets.data import dataset
from assets.select_data import _select_data
from functions.sazonalidade import plot_seasonality
from functions.subseries import plot_subseries
from functions.preprocess import *
from functions.linear import linear


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
    dbc.Row([
        dbc.Col([
            
            dbc.Row(
                html.H4("Base",
                        style={'padding':20})
            ),
            dbc.Row([
           
                dcc.RadioItems(
                    list(dataset.keys()),
                    id='bases',
                    persistence=True, 
                    persistence_type='session',
                    style={'padding':20},
                    # inline=True,
                    value='SINAN',
                    inputStyle={'margin-left': "20px",
                                'margin-right':'3px'}
                    )
                
            ])
            
        ]),
        
        dbc.Col([
            dbc.Row(
                html.H4("Sub-Base",
                        style={'padding':20})
            ),
            
            dbc.Row([
                dcc.Dropdown(options=[],
                    id='dataset',
                    value = 'DOEXT',
                    persistence='bases', 
                    persistence_type='session',
                    placeholder = 'Escolha uma Tabela',
                    searchable=False)
            ])
        ]),
        
        dbc.Col([
            dbc.Row(
                html.H4('Selecione o tipo de gráfico',
                    style={'padding':20}
                )
            ),
            
            dbc.Row(
                dcc.Dropdown(
                    ['Temporal','Sazonalidade','Sub-Séries','Multi-sazonalidade','Defasagens'],
                    value='Temporal',
                    id='plot_type',
                    persistence=True,
                    persistence_type='session', 
                    placeholder = 'Tipo de gráfico',
                    searchable=False
                )
            )
        ])
    ]),
    
    dbc.Row(
        id='filters'    
    ),

    dbc.Row(
        # Grafico
            dcc.Loading(
                    id='plot',
                    type='circle'
                ),
            # width=9
        )

    #     # Filtros
    #     dbc.Col([
    #         html.H4('Selecione os filtros',
    #             style={'padding':20}
    #         ),
    #         dcc.RadioItems(
    #                 ['Diario', 'Mensal', 'Anual'],
    #                 id='agrupamento',
    #                 persistence=True, 
    #                 persistence_type='session',
    #                 style={'padding':20},
    #                 inline=True,
    #                 value='Mensal',
    #                 inputStyle={'margin-left': "20px",
    #                             'margin-right':'3px'}
    #                 ),

    #         dcc.Dropdown(
    #             # filtro_ano,
    #             list(range(1996,2022)),
    #             id='anos',
    #             persistence=True, 
    #             persistence_type='session', 
    #             placeholder = 'Selecione um ano',
    #             multi=True,
    #             searchable=False
    #         )
    #     ]),
    # ]),

    # dbc.Row(dcc.RadioItems(
    #                 ['Nenhum', '1a Diferenciação', '2a Diferenciação', 'Box-Cox_linear', 'Média Móvel', 'Tendência'],
    #                 value = 'Nenhum',
    #                 id='transformacoes_linear',
    #                 persistence=True, 
    #                 persistence_type='session',
    #                 inline=True,
    #                 inputStyle={'margin-left': "20px",
    #                             'margin-right':'3px'}
    #                 )),
    # dbc.Row(dcc.Input(
    #             id='box-cox_linear',
    #             type='text',
    #             # value = 1,
    #             placeholder = 'Selecionar Lambda'
    #         ) )
])

@callback(
    Output(component_id='filters', component_property='children'),
    Input(component_id='plot_type', component_property='value')
)
def filters_function(plot_type):
    child = None
    if plot_type == 'Temporal':
        child =  [
                dbc.Row([
                    dbc.Col([
                        html.H4('Agrupamento',
                            style={'padding':20}
                        ),
                        dcc.RadioItems(
                            ['Diario', 'Mensal', 'Anual'],
                            id='agrupamento_linear',
                            persistence=True, 
                            persistence_type='session',
                            style={'padding':20},
                            inline=True,
                            value='Mensal',
                            inputStyle={'margin-left': "20px",
                                        'margin-right':'3px'}
                            ),
                    ]),
                    
                    dbc.Col([
                        html.H4('Anos',
                        style={'padding':20}
                        ),
                        
                        dcc.Dropdown(
                        # filtro_ano,
                        list(range(1996,2022)),
                        id='anos_linear',
                        persistence=True, 
                        persistence_type='session', 
                        placeholder = 'Selecione um ano',
                        multi=True,
                        searchable=False
                        )
                    ]),
                    
                    dbc.Col([
                        html.H4('Funções',
                        style={'padding':20}
                        ),
                        
                        dcc.RadioItems(
                            ['Nenhum', '1a Diferenciação', '2a Diferenciação', 'Box-Cox', 'Média Móvel', 'Tendência'],
                            value = 'Nenhum',
                            id='transformacoes_linear',
                            persistence=True, 
                            persistence_type='session',
                            # inline=True,
                            inputStyle={'margin-left': "20px",
                                        'margin-right':'3px'}
                        ),
                        
                    ]),
                    
                    dbc.Col([
                        html.H4('Valor Lambda',
                        style={'padding':20}
                        ),
                        
                        dcc.Input(
                            id='box-cox_linear',
                            type='text',
                            # value = 1,
                            placeholder = 'Selecionar Lambda'
                        )
                    ])
                ]),
                
                dbc.Row([
                    dbc.Col(
                        id= 'eixo_sazonalidade'
                    ),
                    dbc.Col(
                        id= 'agrupamento_sazonalidade'
                    )
                ])
            ]
    elif plot_type == 'Sazonalidade':
         child =  [
                dbc.Col([
                    html.H4('Eixo X',
                        style={'padding':20}
                    ),
                    dcc.RadioItems(
                        ['Dia', 'Mes', 'Ano'],
                        id='eixo_sazonalidade',
                        persistence=True, 
                        persistence_type='session',
                        style={'padding':20},
                        inline=True,
                        value='Mes',
                        inputStyle={'margin-left': "20px",
                                    'margin-right':'3px'}
                        )
                ]),
                
                dbc.Col([
                    html.H4('Agrupamento',
                    style={'padding':20}
                    ),
                    
                    dcc.RadioItems(
                        ['Dia', 'Mes', 'Ano'],
                        id='agrupamento_sazonalidade',
                        persistence=True, 
                        persistence_type='session',
                        style={'padding':20},
                        inline=True,
                        value='Ano',
                        inputStyle={'margin-left': "20px",
                                    'margin-right':'3px'}
                        )
                ]),
                dbc.Col([
                    dbc.Row(
                        id= 'agrupamento_linear'
                    ),
                    dbc.Row(
                        id= 'anos_linear'
                    ),
                    dbc.Row(
                        id= 'transformacoes_linear'
                    ),
                    dbc.Row(
                        id= 'box-cox_linear'
                    ),
                ])
            ]
    return child


@callback(
    Output(component_id='plot', component_property='children'),
    Input(component_id='bases', component_property='value'),
    Input(component_id='dataset', component_property='value'),
    Input(component_id='plot_type', component_property='value'),
    Input(component_id='agrupamento_linear', component_property='value'),
    Input(component_id='anos_linear', component_property='value'),
    Input(component_id='transformacoes_linear', component_property='value'),
    Input(component_id='box-cox_linear', component_property='value'),
    Input(component_id='eixo_sazonalidade', component_property='value'),
    Input(component_id='agrupamento_sazonalidade', component_property='value')
)
def data_plot(base_chosen, sub_base, plot_type, agrupamento_linear = None, ano_linear = None, transformacao_linear = None, lambda_box_cox_linear = None, eixo_sazonalidade = None, agrupamento_sazonalidade = None):

    # Resolvendo bug tipo de dado
    if type(sub_base) == list:
        df = dataset[base_chosen][sub_base[0]]
    else:
        df = dataset[base_chosen][sub_base]

    df = df.loc[df['DATA'].apply(lambda x: len(str(x))) > 8]
    # Cria figura
    if plot_type == 'Sazonalidade':
        if  eixo_sazonalidade == agrupamento_sazonalidade:
            return html.H4('Eixo e Agrupamento não podem ser iguais')
        return dcc.Graph(figure = plot_seasonality(df,eixo_sazonalidade, agrupamento_sazonalidade))
    
    elif plot_type == 'Temporal':
        return dcc.Graph(figure = linear(df, base_chosen, ano_linear, agrupamento_linear, transformacao_linear, lambda_box_cox_linear))
    
    elif plot_type == 'Sub-Séries':
        True
        # return dcc.Graph(figure = plot_subseries(df_process,'Data','Casos',title='Gráfico de Sub-Séries'))