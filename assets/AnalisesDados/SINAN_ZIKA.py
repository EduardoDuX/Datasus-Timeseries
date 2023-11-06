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

    # Gráfico de pizza
    fig_pie = px.pie(sinan_zika, names='SEXO')

    # Gráfico de barras empilhadas da distribuição dos casos notificados por sexo
    casos_por_sexo = sinan_zika['SEXO'].groupby(sinan_zika['DATA']).value_counts().reset_index(name='QTD')

    fig_sex = px.line(casos_por_sexo, x = 'DATA', y = 'QTD', color='SEXO')
    fig_sex.update_xaxes(title_text = "Ano")
    fig_sex.update_yaxes(title_text = "Quantidade")



    simdomat_analysis = dbc.Container([
        dbc.Row([
            dbc.Row([
                dbc.Col([
                    dbc.Row(
                        html.H4('Distribuição dos casos notificados por sexo', style={'text-align': 'center'})
                    ),
                    dbc.Row(
                        dcc.Graph(figure= fig_pie)
                    )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'margin-right': '20px', 'padding': 30}),
                dbc.Col([
                    dbc.Row(
                            html.H4('Quantidade de casos de Zika notificados ao longo dos anos por sexo', style={'text-align': 'center'})
                        ),
                        dbc.Row(
                            dcc.Graph(figure= fig_sex)
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