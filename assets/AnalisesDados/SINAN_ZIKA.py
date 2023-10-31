import dash_bootstrap_components as dbc
from assets.data import dataset
from dash import html, dcc, callback, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def return_sinanzika(sinan_zika):

    # Histograma de casos de Zika notificados ao longo dos anos
    notific_anuais = sinan_zika.groupby(pd.to_datetime(sinan_zika['DATA']).dt.year)['DATA'].count().reset_index(name='Total de casos')
    
    fig_ano = px.line(notific_anuais, x = 'DATA', y = 'Total de casos')
    fig_ano.update_xaxes(title_text = "<b>Ano<b>")
    fig_ano.update_yaxes(title_text = "<b>Quantidade<b>")


    simdomat_analysis = dbc.Container([
        dbc.Row([
            dbc.Row([
                dbc.Col([
                    dbc.Row(
                        html.H4('Proporção de Óbitos Maternos por Raça/Cor', style={'text-align': 'center'})
                    ),
                    dbc.Row(
                        # dcc.Graph(figure= fig_raca)
                    )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'margin-right': '20px', 'padding': 30}),
                dbc.Col([
                    dbc.Row(
                            html.H4('Quantidade de Óbitos Maternos por Raça/Cor', style={'text-align': 'center'})
                        ),
                        dbc.Row(
                            # dcc.Graph(figure= fig_bar)
                        )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'padding': 30})
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Row(
                            html.H4('Distribuição de Óbitos Maternos por Raça/Cor e por Ano no período 1996 a 2022', style={'text-align': 'center'})
                        ),
                        dbc.Row(
                            # dcc.Graph(figure= fig_ano)
                        )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'margin-right': '20px', 'padding': 30}),
                
                dbc.Col([
                    dbc.Row(
                            html.H4('', style={'text-align': 'center'})
                        ),
                        dbc.Row(
                            # dcc.Graph(figure= )
                        )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'padding': 30})
            ]),
            
            dbc.Row([
                dbc.Row(
                        html.H4('Quantidade de casos de Zika notificados ao longo dos anos', style={'text-align': 'center'})
                    ),
                    dbc.Row(
                        dcc.Graph(figure= fig_ano)
                    )
            ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'margin-right': '20px', 'padding': 30}
            )
        ])
        
    ])
    return simdomat_analysis