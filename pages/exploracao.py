import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from assets.data import dataset
from assets.select_data import _select_data
from functions.sazonalidade import plot_seasonality
from functions.subseries import plot_subseries
from functions.preprocess import *

dash.register_page(__name__, name='Exploração', title='DATASUS | Exploração')


layout = dbc.Container([
    # Titulo
    dbc.Row([
        dbc.Col(html.H2(['Exploração dos dados']),
                style={'padding':20})
    ]),

    # Seleciona dados
    dbc.Row(_select_data),

    dbc.Row([
        # Grafico
        dbc.Col(
            dcc.Loading(
                    id='plot',
                    type='circle'
                ),
            width=9
        ),

        # Filtros
        dbc.Col([
            html.H4('Selecione os filtros',
                style={'padding':20}
            ),

            dcc.Dropdown(
                list(range(1996,2022)),
                id='anos',
                persistence=True, 
                persistence_type='session', 
                placeholder = 'Selecione um ano',
                searchable=False
            ),
                    
            html.H4('Selecione o tipo de gráfico',
                style={'padding':20}
            ),
            
            dcc.Dropdown(
                ['Temporal','Sazonalidade','Sub-Séries','Multi-sazonalidade','Defasagens'],
                id='plot_type',
                persistence=True,
                persistence_type='session', 
                placeholder = 'Tipo de gráfico',
                searchable=False
            )
        ]),
    ]),

    dbc.Row(dcc.RadioItems(
                    ['1a Diferenciação', '2a Diferenciação', 'Box-Cox', 'Média Móvel'],
                    id='transformacoes',
                    persistence=True, 
                    persistence_type='session',
                    inline=True,
                    inputStyle={'margin-left': "20px",
                                'margin-right':'3px'}
                    ))
])

@callback(
    Output(component_id='plot', component_property='children'),
    Input(component_id='bases', component_property='value'),
    Input(component_id='dataset', component_property='value'),
    Input(component_id='anos', component_property='value'),
    Input(component_id='plot_type', component_property='value')
)
def data_plot(base_chosen, table, ano, plot_type='Temporal'):

    # Resolvendo bug tipo de dado
    if type(table) == list:
        df = dataset[base_chosen][table[0]]
    else:
        df = dataset[base_chosen][table]


    # Preprocessa os dados
    if base_chosen == 'SINAN':
        df = preprocess_SINAN(df)
    elif base_chosen == 'SIM':
        df = preprocess_SIM(df)
    
    # Filtra os dados
    if ano != None:
        df = df[df['Data'].apply(lambda x: x[:4]) == str(ano)]

    # Cria figura
    if plot_type == 'Sazonalidade':
        return dcc.Graph(plot_seasonality(df,'Data','Casos','b', 'Y', title='Gráfico de Sazonalidade'))
    
    elif plot_type == 'Temporal':
        return dcc.Graph(figure = px.line(data_frame=df, x='Data', y='Casos', title=f'Gráfico por tempo'))
    
    elif plot_type == 'Sub-Séries':
        return dcc.Graph(plot_subseries(df,'Data','Casos',title='Gráfico de Sub-Séries'))