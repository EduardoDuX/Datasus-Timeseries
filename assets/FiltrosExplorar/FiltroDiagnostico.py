import dash_bootstrap_components as dbc
from assets.data import dataset
from dash import html, dcc, callback, Input, Output, dash_table


_diag = dbc.Container([
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
                    id='agrupamento_diag',
                    persistence=True, 
                    persistence_type='session',
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
                            html.H4('Parâmetro Q',
                            style={'padding':15}
                            ),
                            style={'text-align': 'center'}
                        ),
                        dbc.Input(
                            id='q',
                            type='text',
                            placeholder = 'Selecionar Q',
                            style = {'margin-bottom': '10px'}
                        )
                    ], style={'border-right': '1px solid black'}),
        dbc.Col([
                        dbc.Row(
                            html.H4('Parâmetro P',
                            style={'padding':15}
                            ),
                            style={'text-align': 'center'}
                        ),
                        dbc.Input(
                            id='p',
                            type='text',
                            placeholder = 'Selecionar P',
                            style = {'margin-bottom': '10px'}
                        )
                    ], style={'border-right': '1px solid black'})
    ])

])