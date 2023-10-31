import dash_bootstrap_components as dbc
from assets.data import dataset
from dash import html, dcc, callback, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def return_simdomat(sim_domat):
    # Distribuição dos óbitos por raca
    fig_raca = px.pie(sim_domat, names='RACA')

    # Barplot de óbitos por raça
    fig_bar = px.histogram(sim_domat, x='RACA', color='RACA')
    fig_bar.update_xaxes(title_text='<b>Raça<b>')
    fig_bar.update_yaxes(title_text='<b>Óbitos<b>')

    # Evolutivo por ano e por raca
    df_agrupado_por_ano = sim_domat.groupby([pd.to_datetime(sim_domat['DATA']).dt.year, 'RACA'])['DATA'].count().reset_index(name='Contagem')

    fig_ano = px.line(df_agrupado_por_ano, x='DATA', y='Contagem', color='RACA')
    fig_ano.update_xaxes(title_text='<b>Ano<b>')
    fig_ano.update_yaxes(title_text='<b>Óbitos<b>')

    # Evolutivo por mes e por raca
    df_agrupado_por_mes = sim_domat.groupby([pd.to_datetime(sim_domat['DATA']).dt.month, 'RACA'])['DATA'].count().reset_index(name='Contagem')

    fig_mes = px.line(df_agrupado_por_mes, x='DATA', y='Contagem', color='RACA')
    fig_mes.update_xaxes(title_text='<b>Mês<b>')
    fig_mes.update_yaxes(title_text='<b>Óbitos<b>')

    # Temporal
    df_agrupado = sim_domat.groupby(pd.to_datetime(sim_domat['DATA']).dt.year)['DATA'].count().reset_index(name='Total de Óbitos')

    fig_temp = px.line(df_agrupado, x='DATA', y='Total de Óbitos')
    fig_temp.update_xaxes(title_text='<b>Ano<b>')
    fig_temp.update_yaxes(title_text='<b>Óbitos<b>')




    simdomat_analysis = dbc.Container([
        dbc.Row([
            dbc.Row([
                dbc.Col([
                    dbc.Row(
                        html.H4('Proporção de Óbitos Maternos por Raça/Cor', style={'text-align': 'center'})
                    ),
                    dbc.Row(
                        dcc.Graph(figure= fig_raca)
                    )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'margin-right': '20px', 'padding': 30}),
                dbc.Col([
                    dbc.Row(
                            html.H4('Quantidade de Óbitos Maternos por Raça/Cor', style={'text-align': 'center'})
                        ),
                        dbc.Row(
                            dcc.Graph(figure= fig_bar)
                        )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'padding': 30})
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Row(
                            html.H4('Distribuição de Óbitos Maternos por Raça/Cor e por Ano no período 1996 a 2022', style={'text-align': 'center'})
                        ),
                        dbc.Row(
                            dcc.Graph(figure= fig_ano)
                        )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'margin-right': '20px', 'padding': 30}),
                
                dbc.Col([
                    dbc.Row(
                            html.H4('Distribuição de Óbitos Maternos por Raça/Cor e Mês no período de 1996 a 2022', style={'text-align': 'center'})
                        ),
                        dbc.Row(
                            dcc.Graph(figure= fig_mes)
                        )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'padding': 30})
            ]),
            
            dbc.Row([
                dbc.Row(
                        html.H4('Distribuição de Óbitos Maternos por Ano no período de 1996 a 2022', style={'text-align': 'center'})
                    ),
                    dbc.Row(
                        dcc.Graph(figure= fig_temp)
                    )
            ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'margin-right': '20px', 'padding': 30}
            )
        ])
        
    ])
    return simdomat_analysis