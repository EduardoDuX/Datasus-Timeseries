import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Diagnóstico', title='DATASUS | Diagnóstico')


layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H3(['Your dataset'])], width=12, className='row-titles')
    ]),


    # Printa figura
    dbc.Row([
        dbc.Col([], width = 2),
        dbc.Col([
            dcc.Loading(id='p1_1-loading', type='circle', children=dcc.Graph(id='fig-pg1', className='my-graph'))
        ], width = 8),
        dbc.Col([], width = 2)
    ], className='row-content')
    
])