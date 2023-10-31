import dash_bootstrap_components as dbc
from assets.data import dataset
from dash import html, dcc, callback, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def return_simdofet(sim_dofet):
    # Distribuição do Sexo
    fig_sexo = px.pie(sim_dofet, names='SEXO')

    # Quantidade de óbitos fetais ao logo dos anos
    sim_dofet['DTOBITO'] = sim_dofet['DTOBITO'].astype(str)
    get_year_death = lambda x: x.split('-')[0]
    sim_dofet['ANOOBITO'] = sim_dofet['DTOBITO'].apply(get_year_death)
    sim_dofet.drop(sim_dofet[sim_dofet['ANOOBITO'] == 'nan'].index, inplace=True)
    deaths_per_gender_counts = sim_dofet['SEXO'].groupby(sim_dofet['ANOOBITO']).value_counts().reset_index(name='QTD')
    fig_obitos_fetais_anos = px.bar(deaths_per_gender_counts, x = 'ANOOBITO', y = 'QTD', color='SEXO')
    fig_obitos_fetais_anos.update_xaxes(title_text = "Ano")
    fig_obitos_fetais_anos.update_yaxes(title_text = "Quantidade")
    
    # Histograma das 30 causas de óbito mais frequentes
    death_freq = sim_doext['CAUSABAS'].value_counts()
    fig_death_freq = px.bar(x=death_freq.index[0:31], y=death_freq.values[0:31])
    fig_death_freq.update_xaxes(title_text = "Código da causa do óbito (CID-10)")
    fig_death_freq.update_yaxes(title_text = "Quantidade de óbitos")

    # Quantidade de óbitos causados por acidentes de trabalho ao logo dos anos
    extract_year = lambda x: x.split('/')[0]
    sim_doext['ANOOBITO'] = sim_doext['DATA'].apply(extract_year)
    sim_doext[['DATA', 'ANOOBITO']].head()
    accident_deaths_counts = sim_doext[sim_doext['ACIDENTE_TRABALHO'] == 'Sim'].value_counts(['ANOOBITO']).reset_index(name='QTD').sort_values(by=['ANOOBITO'])
    fig_qtd_acidente_ano = px.bar(accident_deaths_counts, x = 'ANOOBITO', y = 'QTD')
    fig_qtd_acidente_ano.update_xaxes(title_text = "Ano")
    fig_qtd_acidente_ano.update_yaxes(title_text = "Quantidade")

    # Proporção de tipo de obito sendo ele por afogamento
    df_drowning = sim_doext[sim_doext.CAUSABAS.str.contains("W70", regex=False)]
    labels = df_drowning['ACIDENTE_TRABALHO'].value_counts().index
    values = df_drowning['ACIDENTE_TRABALHO'].value_counts().values
    fig_afogamento = go.Figure(data=[go.Pie(labels=labels, values=values)])
    # fig_afogamento.update(layout_title_text = 'Quantidade de óbitos por afogamento que são (ou não) acidentes')

    # Proporção de tipo de obito sendo ele por transporte
    df_transport = sim_doext[sim_doext.CAUSABAS.str.contains("V87", regex=False)]
    labels = df_transport['ACIDENTE_TRABALHO'].value_counts().index
    values = df_transport['ACIDENTE_TRABALHO'].value_counts().values
    fig_transporte = go.Figure(data=[go.Pie(labels=labels, values=values)])
    # fig_transporte.update(layout_title_text = 'Quantidade de óbitos por acidente de transporte que são (ou não) acidentes')

    simdofet_analysis = dbc.Container([
        dbc.Row([
            dbc.Row([
                dbc.Col([
                    dbc.Row(
                        html.H4('Distribuição das Mortes de Óbitos Fetais por Sexo', style={'text-align': 'center'})
                    ),
                    dbc.Row(
                        dcc.Graph(figure= fig_sexo)
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
    return simdofet_analysis