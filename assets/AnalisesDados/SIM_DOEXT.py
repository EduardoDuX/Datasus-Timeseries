import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def return_simdoext(sim_doext):
    # Distribuições dos Tipos de Óbito
    labels = sim_doext['TIPO'].value_counts().index[1:]
    values = sim_doext['TIPO'].value_counts().values[1:]
    fig_dist_tipo_obito = go.Figure(data=[go.Pie(labels=labels, values=values)])
    # fig_dist_tipo_obito.update(layout_title_text = 'Distribuições dos Tipos de Óbito')

    # Quantidade de óbitos que são (ou não) acidentes
    labels = sim_doext['TRABALHO'].value_counts().index[1:]
    values = sim_doext['TRABALHO'].value_counts().values[1:]
    fig_qtd_obito_acidente = go.Figure(data=[go.Pie(labels=labels, values=values)])
    # fig_qtd_obito_acidente.update(layout_title_text = 'Quantidade de óbitos que são (ou não) acidentes')

    # Histograma das 30 causas de óbito mais frequentes
    death_freq = sim_doext['CAUSA'].value_counts()
    fig_death_freq = px.bar(x=death_freq.index[0:31], y=death_freq.values[0:31])
    fig_death_freq.update_xaxes(title_text = "Código da causa do óbito (CID-10)")
    fig_death_freq.update_yaxes(title_text = "Quantidade de óbitos")

    # Quantidade de óbitos causados por acidentes de trabalho ao logo dos anos
    extract_year = lambda x: x.split('/')[0]
    sim_doext['DATA'] = sim_doext['DATA'].apply(extract_year)
    accident_deaths_counts = sim_doext[sim_doext['TRABALHO'] == 'Sim'].value_counts(['DATA']).reset_index(name='QTD').sort_values(by=['DATA'])
    fig_qtd_acidente_ano = px.bar(accident_deaths_counts, x = 'DATA', y = 'QTD')
    fig_qtd_acidente_ano.update_xaxes(title_text = "Ano")
    fig_qtd_acidente_ano.update_yaxes(title_text = "Quantidade")

    # Proporção de tipo de obito sendo ele por afogamento
    df_drowning = sim_doext[sim_doext.CAUSA.str.contains("W70", regex=False)]
    labels = df_drowning['TRABALHO'].value_counts().index
    values = df_drowning['TRABALHO'].value_counts().values
    fig_afogamento = go.Figure(data=[go.Pie(labels=labels, values=values)])
    # fig_afogamento.update(layout_title_text = 'Quantidade de óbitos por afogamento que são (ou não) acidentes')

    # Proporção de tipo de obito sendo ele por transporte
    df_transport = sim_doext[sim_doext.CAUSA.str.contains("V87", regex=False)]
    labels = df_transport['TRABALHO'].value_counts().index
    values = df_transport['TRABALHO'].value_counts().values
    fig_transporte = go.Figure(data=[go.Pie(labels=labels, values=values)])
    # fig_transporte.update(layout_title_text = 'Quantidade de óbitos por acidente de transporte que são (ou não) acidentes')

    simdoext_analysis = dbc.Container([
        dbc.Row([
            dbc.Row([
                dbc.Col([
                    dbc.Row(
                        html.H4('Distribuição dos Tipos de Óbito', style={'text-align': 'center'})
                    ),
                    dbc.Row(
                        dcc.Graph(figure= fig_dist_tipo_obito)
                    )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'margin-right': '20px', 'padding': 30}),
                dbc.Col([
                    dbc.Row(
                            html.H4('Distribuição de óbitos para acidentes', style={'text-align': 'center'})
                        ),
                        dbc.Row(
                            dcc.Graph(figure= fig_qtd_obito_acidente)
                        )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'padding': 30})
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Row(
                            html.H4('Quantidade de óbitos por afogamento que são (ou não) acidentes', style={'text-align': 'center'})
                        ),
                        dbc.Row(
                            dcc.Graph(figure= fig_afogamento)
                        )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'margin-right': '20px', 'padding': 30}),
                
                dbc.Col([
                    dbc.Row(
                            html.H4('Quantidade de óbitos por acidente de transporte que são (ou não) acidentes', style={'text-align': 'center'})
                        ),
                        dbc.Row(
                            dcc.Graph(figure= fig_transporte)
                        )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'padding': 30})
            ]),
            
            dbc.Row([
                dbc.Row(
                        html.H4('Causas de óbito não naturais mais frequentes', style={'text-align': 'center'})
                    ),
                    dbc.Row(
                        dcc.Graph(figure= fig_death_freq)
                    )
            ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'margin-right': '20px', 'padding': 30}
            ),
            
        
            dbc.Row([
                dbc.Row(
                        html.H4('Quantidade de óbitos causados por acidentes de trabalho ao logo dos anos', style={'text-align': 'center'})
                    ),
                    dbc.Row(
                        dcc.Graph(figure= fig_qtd_acidente_ano)
                    )
            ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'padding': 30}
            )            
            
            
        ])
        
    ])
    return simdoext_analysis