import dash_bootstrap_components as dbc
from dash import dcc,html
from assets.data import dataset

_select_data = dbc.Container([
            dbc.Row(
                html.H4("Selecione a base que deseja utilizar",
                        style={'padding':20})
            ),
            dbc.Col([
                dbc.Row(
                dcc.RadioItems(
                    list(dataset.keys()),
                    id='bases',
                    persistence=True, 
                    persistence_type='session',
                    style={'padding':20},
                    inline=True,
                    value='SINAN',
                    inputStyle={'margin-left': "20px",
                                'margin-right':'3px'}
                    )),
                dcc.Dropdown(options=[],
                        id='dataset',
                        value = 'DOEXT',
                        persistence='bases', 
                        persistence_type='session',
                        placeholder = 'Escolha uma Tabela',
                        searchable=False)
            ])
    ])