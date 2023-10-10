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
    dbc.Row(_select_data),

    # Tabela
    dbc.Row([
        dbc.Col([
            dcc.Loading(id='table_loading',
                        type='circle',
                        children=dash_table.DataTable(id='data_table',
                                                        page_size=11, 
                                                        style_table={'overflowX': 'auto'}), 
                                                        style={'border-radius': 25, 'padding':20})
        ])
    ])

]),

@callback(
    Output(component_id='dataset', component_property='options'),
    Output(component_id='dataset', component_property='value'),
    Input(component_id='bases', component_property='value')
)
def update_database(base_chosen):

    if base_chosen != None:
        df_options = list(dataset[base_chosen].keys())
        return df_options, df_options


@callback(
    Output(component_id='data_table', component_property='data'),
    Input(component_id='bases', component_property='value'),
    Input(component_id='dataset', component_property='value')
)
def data_table(base_chosen, table):

    if base_chosen != None and table != None:
        df = dataset[base_chosen][table].to_dict('records')
        return df

# @callback(
#     Output(component_id='bases_descript', component_property='children'),
#     Input(component_id='bases', component_property='value')
# )
# def descricao_base(bas):
#     if bas == 'SINAN':
#         return "O SINAN é o sistema responsável por registrar a 
# ocorrências de doenças e agravos que constam da lista nacional de do
# enças de notificação compulsória desde 1979. Cada estado e município tem a 
# liberdade de incluir outros problemas de saúde que sejam importantes para sua 
# região. Os registros podem variar desde Doença de Chagas, Tétano à Violência Dom
# éstica. Como cada doença ou agravo possui sua própria base de registro, os tipos d
# e dados registrados podem variar muito, porém as bases tem suas semelhanças, como o 
# registro de data de ocorrência, local de ocorrência e dados sobre o paciente."
#     else:
#         return "O SIM é responsável por coletar, armazenar e disponibiliz
# ar dados sobre óbitos ocorridos em todo território brasileiro. Ele registr
# a diversas informações sobre a morte, como a data/hora e local do ocorrido,
#  identificação e perfil socioeconômico do paciente, causa da morte, informaçõ
# es do Certificado de Morte e tipo de assistência médica recebida. Além disso,
#  o sistema fornece dados sobre óbitos de crianças (neonatais e infantis) e inf
# ormações sobre a mãe"