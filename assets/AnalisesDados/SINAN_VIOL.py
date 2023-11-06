import dash_bootstrap_components as dbc
from assets.data import dataset
from dash import html, dcc, callback, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def return_sinanviol(sinan_viol):

    # Gráfico de pizza
    fig_sex = px.pie(sinan_viol, names='SEXO')

    # Gráfico de pizza
    fig_raca = px.pie(sinan_viol, names='RACA')

    # Histograma de ocorrências ao longo dos anos
    notific_anuais = sinan_viol.value_counts(['DATA']).reset_index(name='QTD').sort_values(by=['DATA'])

    fig_temp = px.line(notific_anuais, x = 'DATA', y = 'QTD')
    fig_temp.update_xaxes(title_text = "Ano")
    fig_temp.update_yaxes(title_text = "Quantidade")

    # Idade
    sinan_viol['DATASTR'] = sinan_viol['DATA'].astype(str)

    sinan_viol['ANO_OCOR'] = sinan_viol['DATASTR'].apply(lambda x: x.split('-')[0])

    sinan_viol['IDADE'] = sinan_viol['ANO_OCOR'].astype(float) - sinan_viol['ANO_NASC']
    idades = sinan_viol.value_counts(['IDADE']).reset_index(name='QTD').sort_values(by=['IDADE'], ascending = False)
    idades.drop(idades.loc[idades['IDADE'] < 0].index, inplace=True)
    idades.drop(idades.loc[idades['IDADE'] > 200].index, inplace=True)
    sinan_viol.loc[sinan_viol['IDADE'] <= 10, 'FAIXA_ETARIA'] = 'Até 10 anos'
    sinan_viol.loc[(sinan_viol['IDADE'] > 10) & (sinan_viol['IDADE'] <= 20), 'FAIXA_ETARIA'] = 'De 11 a 20 anos'
    sinan_viol.loc[(sinan_viol['IDADE'] > 20) & (sinan_viol['IDADE'] <= 30), 'FAIXA_ETARIA'] = 'De 21 a 30 anos'
    sinan_viol.loc[(sinan_viol['IDADE'] > 30) & (sinan_viol['IDADE'] <= 40), 'FAIXA_ETARIA'] = 'De 31 a 40 anos'
    sinan_viol.loc[(sinan_viol['IDADE'] > 40) & (sinan_viol['IDADE'] <= 60), 'FAIXA_ETARIA'] = 'De 41 a 60 anos'
    sinan_viol.loc[sinan_viol['IDADE'] > 60, 'FAIXA_ETARIA'] = 'Mais de 60 anos'
    faixa_etaria = sinan_viol.value_counts(['FAIXA_ETARIA']).reset_index(name='QTD').sort_values(by=['FAIXA_ETARIA'], ascending = False)

    # Histograma de ocorrências ao longo dos dias
    fig_age = px.bar(faixa_etaria, x = 'FAIXA_ETARIA', y = 'QTD')
    fig_age.update_xaxes(title_text = "Faixas Etárias")
    fig_age.update_yaxes(title_text = "Quantidade")
    

    simdomat_analysis = dbc.Container([
        dbc.Row([
            dbc.Row([
                dbc.Col([
                    dbc.Row(
                        html.H4('Distribuição de ocorrências por sexo', style={'text-align': 'center'})
                    ),
                    dbc.Row(
                        dcc.Graph(figure= fig_sex)
                    )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'margin-right': '20px', 'padding': 30}),
                dbc.Col([
                    dbc.Row(
                            html.H4('Distribuição de ocorrências por raça', style={'text-align': 'center'})
                        ),
                        dbc.Row(
                            dcc.Graph(figure= fig_raca)
                        )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'padding': 30})
            ]),

            dbc.Row([
                dbc.Row(
                        html.H4('Distribuição de idades', style={'text-align': 'center'})
                    ),
                    dbc.Row(
                        dcc.Graph(figure= fig_age)
                    )
            ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'margin-right': '20px', 'padding': 30}
            ),
            
            dbc.Row([
                dbc.Row(
                        html.H4('Quantidade de ocorrências notificadas ao longo dos anos', style={'text-align': 'center'})
                    ),
                    dbc.Row(
                        dcc.Graph(figure= fig_temp)
                    )
            ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'margin-right': '20px', 'padding': 30}
            )
        ])
        
    ])
    return simdomat_analysis