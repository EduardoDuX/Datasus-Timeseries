import dash_bootstrap_components as dbc
from assets.data import dataset
from dash import html, dcc, callback, Input, Output

_select_data = dbc.Container([
    dbc.Row([
            dbc.Col([
            # , 'margin-left': '25px', 'width': '100%'
            dbc.Row(
                html.H4("Base",
                        style={'padding':10, 'text-align': 'center'})
            ),
            dbc.Row([
           
                dcc.RadioItems(
                    list(dataset.keys()),
                    id='bases',
                    style={'padding':5},
                    inline=True,
                    value='SINAN',
                    inputStyle={'margin-left': "20px",
                                'margin-right':'3px'}
                    )
                
            ], style={'text-align': 'center'}
            )
            
        ], style={'border-right': '1px solid black'}),

        
        # Seleciona Sub-Base
        dbc.Col([
            dbc.Row(
                html.H4("Sub-Base",
                        style={'padding':10, 'text-align': 'center'})
            ),
            
            dbc.Row([
                dbc.Col(width=2),
                dbc.Col(
                    dcc.Dropdown(
                        id='dataset',
                        placeholder = 'Escolha uma Tabela',
                        style={'margin-bottom': '10px'},
                        searchable=False)
                ),
                dbc.Col(width=2)
            ], style={'text-align': 'center'})
        ]),
    ], justify = 'center')
])


@callback(
    Output(component_id='dataset', component_property='options'),
    Output(component_id='dataset', component_property='value'),
    Input(component_id='bases', component_property='value')
)
def update_database(base_chosen):

    if base_chosen != None:
        df_options = list(dataset[base_chosen].keys())
        return df_options, df_options[0]