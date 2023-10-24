import dash_bootstrap_components as dbc
from dash import dcc,html
from assets.data import dataset

_sazonalidade = dbc.Container([
            
                dbc.Row([
                    dbc.Col([
                        dbc.Row(
                            html.H4('Eixo X',
                                style={'padding':20, 'text-align': 'center'}
                            ),
                            style={'text-align': 'center'}
                        ),
                        dbc.Row(
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
                                ),
                            style={'text-align': 'center'}
                        )
                    ], style={'border-right': '1px solid black'}),
                    
                    dbc.Col([
                        dbc.Row(
                            html.H4('Agrupamento',
                            style={'padding':20, 'text-align': 'center'}
                            ),
                            style={'text-align': 'center'}
                        ),
                        dbc.Row(
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
                                ),
                            style={'text-align': 'center'}
                        )
                    ])
                ]),
                dbc.Row([
                    dbc.Col(
                        id= 'agrupamento_linear'
                    ),
                    dbc.Col(
                        id= 'anos_linear'
                    ),
                    dbc.Col(
                        id= 'transformacoes_linear'
                    ),
                    dbc.Col(
                        id= 'box-cox_linear'
                    ),
                    dbc.Col(
                        id= 'lags_autocorr'
                    ),
                    dbc.Col(
                        id= 'agrupamento_autocorr'
                    ),
                    dbc.Col(
                        id= 'pacf_autocorr'
                    )
                    
                ])
            ])