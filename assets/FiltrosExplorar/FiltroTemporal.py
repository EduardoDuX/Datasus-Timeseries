import dash_bootstrap_components as dbc
from dash import dcc,html
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
                        list(range(1996,1522)),
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
                            ['Nenhum', '1a Diferenciação', '2a Diferenciação', 'Box-Cox', 'Média Móvel', 'Tendência'],
                            value = 'Nenhum',
                            id='transformacoes_linear',
                            persistence=True, 
                            persistence_type='session',
                            style = {'margin-bottom': '10px'}
                        ),
                        
                    ], style={'border-right': '1px solid black'}),
                    

                    dbc.Col([
                        dbc.Row(
                            html.H4('Valor Lambda',
                            style={'padding':15}
                            ),
                            style={'text-align': 'center'}
                        ),
                        dbc.Input(
                            id='box-cox_linear',
                            type='text',
                            # value = 1,
                            placeholder = 'Selecionar Lambda',
                            style = {'margin-bottom': '10px'}
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
                ], style={'background-color' : 'red'})
            ])