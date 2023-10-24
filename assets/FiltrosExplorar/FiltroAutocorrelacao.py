import dash_bootstrap_components as dbc
from assets.data import dataset
from dash import html, dcc, callback, Input, Output, dash_table


_autocorr = dbc.Container([
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
                    id='agrupamento_autocorr',
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
                                        'margin-right':'5px'}
                            # style = {'margin-bottom': '10px'}
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
            id= 'parametro_linear'
        ),
        dbc.Col(
            id= 'eixo_sazonalidade'
        ),
        dbc.Col(
            id= 'agrupamento_sazonalidade'
        )
    ])

])