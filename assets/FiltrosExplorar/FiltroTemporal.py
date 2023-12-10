import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output
from assets.data import dataset

_temporal = dbc.Container([
                dbc.Row([
                    dbc.Col([
                        dbc.Row(
                        html.H4('Agrupamento',
                                style={'padding':15}
                            ),
                            style={'text-align': 'center'}
                        ),
                        dbc.Row(
                            dcc.RadioItems(

                                ['Diario', 'Mensal', 'Anual'],
                                id='agrupamento_linear',
                                persistence=True, 
                                persistence_type='session',
                                # style={'padding':15},
                                inline=True,
                                value='Mensal',
                                inputStyle={'margin-left': "5px",
                                            'margin-right':'5px'}
                                ),
                            style={'text-align': 'center'}
                        )
                    ], style={'border-right': '1px solid black'}),


                    dbc.Col([
                        dbc.Row(
                            html.H4('Anos',
                            style={'padding':15}
                            ),
                            style={'text-align': 'center'}
                        ),
                        dcc.Dropdown(
                        # filtro_ano,
                        list(range(1996,2022)),
                        value = [],
                        id='anos_linear',
                        persistence=True, 
                        persistence_type='session', 
                        placeholder = 'Selecione um ano',
                        multi=True,
                        searchable=False,
                        style = {'margin-bottom': '10px'}
                        )
                    ], style={'border-right': '1px solid black'}),
                    

                    dbc.Col([
                        dbc.Row(
                            html.H4('Funções',
                            style={'padding':15}
                            ),
                            style={'text-align': 'center'}
                        ),
                        dcc.Dropdown(
                            ['Nenhum', '1a Diferenciação', '2a Diferenciação', 'Box-Cox', 'Média Móvel', 'Tendência', 'Estacionariedade', 'Autocorrelação'],
                            value = 'Nenhum',
                            id='transformacoes_linear',
                            persistence=True,
                            persistence_type='session',
                            style = {'margin-bottom': '10px'}
                        ),
                        
                    ]),
                    
                    
                ]),
                
                dbc.Row(
                        id = 'extra_param'
                    ),
                
                dbc.Row([
                
                    dbc.Col(
                        id= 'eixo_sazonalidade'
                    ),
                    dbc.Col(
                        id= 'agrupamento_sazonalidade'
                    ),
                    # dbc.Col(
                    #     id= 'lags_autocorr'
                    # ),
                    dbc.Col(
                        id= 'agrupamento_autocorr'
                    ),
                    # dbc.Col(
                    #     id= 'pacf_autocorr'
                    # )
                ], style={'background-color' : 'red'})
            ])

# @callback(
#     Output(component_id='box-cox_linear', component_property='disabled'),
#     Input(component_id='transformacoes_linear', component_property='value')
# )
# def input_activation(transformacao):
#     if transformacao == 'Box-Cox' or transformacao == 'Média Móvel':
#         return False
#     else:
#         return True
    
@callback(
    Output(component_id='extra_param', component_property='children'),
    Input(component_id='transformacoes_linear', component_property='value')
)
def input_activation(transformacao):
    if transformacao == 'Box-Cox' or transformacao == 'Média Móvel':
        titulo = ''
        if transformacao == 'Box-Cox':
            titulo = 'Valor Lambda'
        else:
            titulo = 'Quantidade Médias'
        return [
                dbc.Row([
                        dbc.Row(
                            html.H4(titulo,
                            style={'padding':15}
                            ),
                            style={'text-align': 'center'}
                        ),
                        dbc.Input(
                            id='param_linear',
                            type='text',
                            # value = 1,
                            placeholder = 'Selecionar Valor',
                            style = {'margin-bottom': '10px'}
                        )
                    ]),
                dbc.Row([
                    dbc.Col(
                        id= 'lags_autocorr'
                    ),
                    dbc.Col(
                        id= 'pacf_autocorr'
                    )
                ])
                ]
    elif transformacao == 'Autocorrelação':
        return [
                    dbc.Row([
                        dbc.Col([
                                    dbc.Row(
                                        html.H4('Quantidade Lags',
                                        style={'padding':15}
                                        ),
                                        style={'text-align': 'center'}
                                    ),
                                    dbc.Input(
                                        id='lags_autocorr',
                                        type='text',
                                        placeholder = 'Selecionar Lags',
                                        style = {'margin-bottom': '10px'}
                                    )
                                ], style={'border-right': '1px solid black'}),
                        dbc.Col([
                                    dbc.Row(
                                        html.H4('ACF ou PACF',
                                        style={'padding':15}
                                        ),
                                        style={'text-align': 'center'}
                                    ),
                                    dbc.RadioItems(
                                        ['ACF', 'PACF'],
                                        id='pacf_autocorr',
                                        persistence=True, 
                                        persistence_type='session',
                                        # style={'padding':15},
                                        inline=True,
                                        value='ACF',
                                        inputStyle={'margin-left': "5px",
                                                    'margin-right':'5px'},
                                        style={'text-align': 'center'}
                                    )
                                ], style={'text-align': 'center'})
                    ]),
                    dbc.Row(id='param_linear')
        ]
    else:
        return [
            dbc.Row([
                    dbc.Col(
                        id= 'lags_autocorr'
                    ),
                    dbc.Col(
                        id= 'pacf_autocorr'
                    ),
                    dbc.Col(
                        id= 'param_linear'
                    )
                ])
        ]
