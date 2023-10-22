import dash
from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
from assets.data import dataset
from assets.select_data import _select_data

dash.register_page(__name__, name='Dados', title='DATASUS | Dados')


layout = dbc.Container([
    # Titulo
    dbc.Row([
        dbc.Col(html.H2(['Seleção dos dados']),
                style={'padding':20})
    ]),

    # Selecao de dados
    dbc.Row(_select_data, style={'background-color':'#BDC3C7', 'border-radius': '10px', 'margin-bottom':'20px'}),
    dbc.Row([dbc.Col([], width = 1)]),
    # Tabela
    dbc.Row([
        dbc.Row([
            dbc.Col([
                dbc.Row(html.H3(['Descrição Base']), style={'padding':20, 'text-align': 'center'}),
                dbc.Row(
                id='descricao_base'
                )
            ]),
            dbc.Col([
                dbc.Row(html.H3(['Descrição Sub-Base']), style={'padding':20, 'text-align': 'center'}),
                dbc.Row(
                id='descricao_sub-base'
                )
            ])
            ], style={'background-color': '#415A77', 'border-radius': '15px', 'margin-bottom': '20px'}
        ),

        dbc.Row([
            dbc.Col([
                dbc.Row(html.H5(['Quantidade de Registros']), style={'padding':20, 'text-align': 'center'}),
                dbc.Row(
                id='registros_base'
                )
            ]),
            dbc.Col([
                dbc.Row(html.H5(['Anos Registrados']), style={'padding':20, 'text-align': 'center'}),
                dbc.Row(
                id='anos_base'
                )
            ]),
            dbc.Col(
                id='extra_base'
            )
            ], style={'background-color': '#BDC3C7', 'border-radius': '15px', 'margin-bottom': '20px'}
        ),

        dbc.Row(
            html.H3('Tabela Exemplo', style={'padding': 15, 'text-align': 'center'})
        ),

        dbc.Row(
            dcc.Loading(id='table_loading',
                        type='circle',
                        children=dash_table.DataTable(id='data_table',
                                                        page_size=11, 
                                                        style_table={'overflowX': 'auto'}), 
                                                        style={'border-radius': 25, 'padding':20, 'background-color': '#E0E1DD', 'color': '#E0E1DD'})
        )
    ], style={'background-color': '778DA9', 'min-width': '200px', 'min-height': '300px', 'padding':20, 'border-radius': '15px', 'margin-bottom': '20px'})

]),

@callback(
    Output(component_id='descricao_base', component_property='children'),
    Output(component_id='descricao_sub-base', component_property='children'),
    Input(component_id='bases', component_property='value'),
    Input(component_id='dataset', component_property='value')
)
def update_database(base, sub_base):
    if base == 'SIM':
        desc_base = html.Div([
            html.H5('Sistema de Informação sobre a Mortalidade', style={'text-align': 'center'}),
            html.P('O SIM é responsável por coletar, armazenar e disponibilizar dados sobre óbitos ocorridos em todo território brasileiro. Ele registra diversas informações sobre a morte, como a data/hora e local do ocorrido, identificação e perfil socioeconômico do paciente, causa da morte, informações do Certificado de Morte e tipo de assistência médica recebida. Além disso, o sistema fornece dados sobre óbitos de crianças (neonatais e infantis) e informações sobre a mãe',
            style={'text-align': 'justify'})
        ])
    else:
        desc_base = html.Div([
            html.H5('Sistema de Informações de Agravos de Notificação', style={'text-align': 'center'}),
            html.P('O SINAN é o sistema responsável por registrar a ocorrências de doenças e agravos que constam da lista nacional de doenças de notificação compulsória desde 1979. Cada estado e município tem a liberdade de incluir outros problemas de saúde que sejam importantes para sua região. Os registros podem variar desde Doença de Chagas, Tétano à Violência Doméstica. Como cada doença ou agravo possui sua própria base de registro, os tipos de dados registrados podem variar muito, porém as bases tem suas semelhanças, como o registro de data de ocorrência, local de ocorrência e dados sobre o paciente.',
            style={'text-align': 'justify'})
        ])
    
    desc_sub_base = None
    return desc_base, desc_sub_base


@callback(
    Output(component_id='data_table', component_property='data'),
    Output(component_id='registros_base', component_property='children'),
    Output(component_id='anos_base', component_property='children'),
    Input(component_id='bases', component_property='value'),
    Input(component_id='dataset', component_property='value')
)
def data_table(base_chosen, table):

    df = dataset[base_chosen][table]

    tam = html.P(f'A base possui {len(df)} registros', style={'text-align': 'center'})

    anos = list(df['DATA'].apply(lambda x: str(x)[:4]).unique())
    range_anos = html.P(f'Os anos variam entre {min(anos)}-{max(anos)}', style={'text-align': 'center'})

    tab = df.head().to_dict('records')
    return tab, tam, range_anos
