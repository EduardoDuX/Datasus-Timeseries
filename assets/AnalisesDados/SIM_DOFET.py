import dash_bootstrap_components as dbc
from assets.data import dataset
from dash import html, dcc, callback, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def return_simdofet(sim_dofet):
    

    # Preprocessamento
    get_gender = lambda x: "M" if x == '1.0' or x == '1' else ("F" if x == '2.0' or x == '2' else "I")
    sim_dofet['SEXO'] = sim_dofet['SEXO'].apply(get_gender)
    sim_dofet.head()

    # Distribuição do Sexo
    fig_sexo = px.pie(sim_dofet, names='SEXO')

    # Distribuicao do sexo no tempo
    get_year_death = lambda x: str(x).split('-')[0]
    sim_dofet['ANOOBITO'] = sim_dofet['DATA'].apply(get_year_death)
    sim_dofet.drop(sim_dofet[sim_dofet['ANOOBITO'] == 'nan'].index, inplace=True)
    deaths_per_gender_counts = sim_dofet['SEXO'].groupby(sim_dofet['ANOOBITO']).value_counts().reset_index(name='QTD')
    fig_sexo_temp = px.bar(deaths_per_gender_counts, x = 'ANOOBITO', y = 'QTD', color='SEXO')

    # Distribuicao do peso dos fetos por ano
    sim_dofet['PESO'] = sim_dofet['PESO'].str.replace(' ','.').astype(float)
    df_plot = sim_dofet[['PESO','ANOOBITO']].groupby('ANOOBITO').mean().reset_index()
    fig_peso_temp = px.line(df_plot, x = 'ANOOBITO', y = 'PESO')
    fig_peso_temp.update_xaxes(title_text = "Ano")
    fig_peso_temp.update_yaxes(title_text = "Peso médio")
    

    simdofet_analysis = dbc.Container([
        dbc.Row([
            dbc.Row([
                dbc.Col([
                    dbc.Row(
                        html.H4('Distribuição das Mortes de Óbitos Fetais por Sexo', style={'text-align': 'center'})
                    ),
                    dbc.Row(
                        dcc.Graph(figure = fig_sexo)
                    )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'margin-right': '20px', 'padding': 30}),
                dbc.Col([
                    dbc.Row(
                            html.H4('Quantidade de óbitos fetais ao logo dos anos', style={'text-align': 'center'})
                        ),
                        dbc.Row(
                            dcc.Graph(figure = fig_sexo_temp)
                        )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'padding': 30})
            ]),
            
            dbc.Row([
                dbc.Row(
                        html.H4('Peso médio dos óbitos fetais por ano', style={'text-align': 'center'})
                    ),
                    dbc.Row(
                        dcc.Graph(figure = fig_peso_temp)
                    )
            ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'margin-right': '20px', 'padding': 30}
            )    
        ])
        
    ])
    return simdofet_analysis