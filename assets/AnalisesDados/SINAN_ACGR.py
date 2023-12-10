import dash_bootstrap_components as dbc
from assets.data import dataset
from dash import html, dcc, callback, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

def calcular_idade(row, ano_desejado):
        ano_atual = date.today().year
        idade = ano_desejado - row['ANO_NASC']
        return idade

def return_sinanacgr(sinan_acgr):

    # Processamento
    sinan_acgr.dropna(inplace = True)
    

    ano_desejado = 2022

    sinan_acgr['IDADE'] = sinan_acgr.apply(calcular_idade, args=(ano_desejado,), axis=1)
    sinan_acgr['IDADE'] = sinan_acgr['IDADE'].astype('category')


    # Como a frequência dos acidentes de trabalho varia conforme a idade da vítima?
    df_p1 = sinan_acgr.groupby(by = 'IDADE').count().reset_index()
    df_p1 = df_p1[['IDADE','ID']]

    fig_idade = px.bar(df_p1, x = 'IDADE', y = 'ID')
    fig_idade.update_xaxes(title_text = "Idade")
    fig_idade.update_yaxes(title_text = "Quantidade")

    # Qual a lesão mais comum em acidentes de trabalho no Brasil?
    df_p2 = sinan_acgr['CID_LESAO'].value_counts().reset_index()
    df_p2.rename(columns={"index": "CID_LESAO", "CID_LESAO": "quantidade"}, inplace = True)

    df_p2 = df_p2.head(5)

    fig_lesao = px.bar(df_p2, x = 'CID_LESAO', y = 'quantidade')
    fig_lesao.update_xaxes(title_text = "Lesão (CID-10)")
    fig_lesao.update_yaxes(title_text = "Quantidade")

    # Existe alguma diferença na proporção de ocorrências de acidentes de trabalho por raça/cor?
    df_p1 = sinan_acgr.groupby(by = 'RACA').count().reset_index()
    df_p1 = df_p1[['RACA','ID']]

    fig_raca = px.bar(df_p1, x = 'RACA', y = 'ID')
    fig_raca.update_xaxes(title_text = "RACA")
    fig_raca.update_yaxes(title_text = "Quantidade")

    sinanacgr_analysis = dbc.Container([
        dbc.Row([
            dbc.Row([
                dbc.Col([
                    dbc.Row(
                        html.H4('Acidentes de trabalho pela idade da vítima', style={'text-align': 'center'})
                    ),
                    dbc.Row(
                        dcc.Graph(figure= fig_idade)
                    )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'margin-right': '20px', 'padding': 30}),
                dbc.Col([
                    dbc.Row(
                            html.H4('Quantidade dos 5 tipos de lesões mais comuns no Brasil', style={'text-align': 'center'})
                        ),
                        dbc.Row(
                            dcc.Graph(figure= fig_lesao)
                        )
                ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'padding': 30})
            ]),
            
            dbc.Row([
                dbc.Row(
                        html.H4('Acidentes de trabalho pela raça/cor da vítima', style={'text-align': 'center'})
                    ),
                    dbc.Row(
                        dcc.Graph(figure= fig_raca)
                    )
            ], style={'border-radius': '15px', 'background-color': '#BDC3C7', 'margin-bottom': '20px', 'margin-right': '20px', 'padding': 30}
            )
        ])
        
    ])
    return sinanacgr_analysis