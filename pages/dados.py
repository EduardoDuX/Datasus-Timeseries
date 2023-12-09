import dash
from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
from assets.data import dataset
from assets.select_data import _select_data
from assets.AnalisesDados.SIM_DOEXT import return_simdoext
from assets.AnalisesDados.SIM_DOMAT import return_simdomat
from assets.AnalisesDados.SINAN_ZIKA import return_sinanzika
from assets.AnalisesDados.SINAN_VIOL import return_sinanviol
from assets.AnalisesDados.SIM_DOFET import return_simdofet

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
                dbc.Row(html.H3(['Descrição Base']), style={'padding':20, 'text-align': 'center', 'color': 'white'}),
                dbc.Row(
                id='descricao_base'
                )
            ]),
            dbc.Col([
                dbc.Row(html.H3(['Descrição Sub-Base']), style={'padding':20, 'text-align': 'center', 'color': 'white'}),
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
        ),
        
        dbc.Row(
            html.H3('Análise Exploratória dos Dados', style={'padding': 15, 'text-align': 'center'})
        ),
        
        dbc.Row(dcc.Loading(id='explorar', type='circle'))
        
    ], style={'background-color': '778DA9', 'min-width': '200px', 'min-height': '300px', 'padding':20, 'border-radius': '15px', 'margin-bottom': '20px'})

]),

# Atualiza Textos
@callback(
    Output(component_id='descricao_base', component_property='children'),
    Output(component_id='descricao_sub-base', component_property='children'),
    Input(component_id='bases', component_property='value'),
    Input(component_id='dataset', component_property='value')
)
def update_database(base, sub_base):
    if base == 'SIM':
        desc_base = html.Div([
            html.H5('Sistema de Informação sobre a Mortalidade', style={'text-align': 'center', 'color': 'white'}),
            html.P('O SIM é responsável por coletar, armazenar e disponibilizar dados sobre óbitos ocorridos em todo território brasileiro. Ele registra diversas informações sobre a morte, como a data/hora e local do ocorrido, identificação e perfil socioeconômico do paciente, causa da morte, informações do Certificado de Morte e tipo de assistência médica recebida. Além disso, o sistema fornece dados sobre óbitos de crianças (neonatais e infantis) e informações sobre a mãe',
            style={'text-align': 'justify', 'color': 'white'})
        ])
    else:
        desc_base = html.Div([
            html.H5('Sistema de Informações de Agravos de Notificação', style={'text-align': 'center', 'color': 'white'}),
            html.P('O SINAN é o sistema responsável por registrar a ocorrências de doenças e agravos que constam da lista nacional de doenças de notificação compulsória desde 1979. Cada estado e município tem a liberdade de incluir outros problemas de saúde que sejam importantes para sua região. Os registros podem variar desde Doença de Chagas, Tétano à Violência Doméstica. Como cada doença ou agravo possui sua própria base de registro, os tipos de dados registrados podem variar muito, porém as bases tem suas semelhanças, como o registro de data de ocorrência, local de ocorrência e dados sobre o paciente.',
            style={'text-align': 'justify', 'color': 'white'})
        ])
    
    if sub_base == 'ZIKA':

        desc_sub_base = html.Div([
            html.P('A base SINAN-ZIKA de zika é uma parte do Sistema de Informação de Agravos de Notificação (SINAN), que é alimentado com dados das notificações de casos de zika.',
            style={'text-align': 'justify', 'color': 'white'})
        ])

    elif sub_base == 'VIOL':

        desc_sub_base = html.Div([
            html.P('''A base SINAN-VIOL de violência é uma parte do Sistema de Informação de Agravos de Notificação (SINAN), que é alimentado com dados das notificações de casos de violência. 

Os casos suspeitos ou confirmados de violência doméstica/intrafamiliar, sexual, autoprovocada, tráfico de pessoas, trabalho escravo, trabalho infantil, tortura, intervenção legal e violências homofóbicas contra mulheres e homens em todas as idades são objetos de notificação.''',
            style={'text-align': 'justify', 'color': 'white'})
        ])

    elif sub_base == 'ACGR':

        desc_sub_base = html.Div([
            html.P('''A base SINAN-ACGR de acidentes de trabalho é uma parte do Sistema de Informação de Agravos de Notificação (SINAN). Esta base é alimentada com dados das notificações de casos de acidentes de trabalho. 

Os acidentes de trabalho são definidos como aqueles que ocorrem no ambiente de trabalho ou durante o exercício do trabalho quando o trabalhador estiver realizando atividades relacionadas à sua função, ou a serviço do empregador ou representando os interesses do mesmo (Típico) ou no percurso entre a residência e o trabalho (Trajeto) que provoca lesão corporal ou perturbação funcional, podendo causar a perda ou redução temporária ou permanente da capacidade para o trabalho e morte.''',
            style={'text-align': 'justify', 'color': 'white'})
        ])
    
    elif sub_base == 'DOMAT':

        desc_sub_base = html.Div([
            html.P('''Similar a base SIM-DO, essa base de dados contém informações sobre óbitos maternos, que são aqueles que ocorrem durante a gravidez ou até 42 dias após o término da gestação, independentemente da duração ou localização da gravidez.''',
            style={'text-align': 'justify', 'color': 'white'})
        ])

    elif sub_base == 'DOFET':

        desc_sub_base = html.Div([
            html.P('''Similar a base SIM-DO, essa base de dados contém informações sobre óbitos fetais, que são aqueles que ocorrem antes do nascimento. Esses dados são fundamentais para entender os aspectos referentes à mortalidade fetal no Brasil e às causas que levaram ao óbito.
''',
            style={'text-align': 'justify', 'color': 'white'})
        ])

    elif sub_base == 'DOEXT':

        desc_sub_base = html.Div([
            html.P('''Similar a base SIM-DO, essa base de dados contém informações sobre óbitos que ocorreram devido a causas externas. As causas externas são aquelas que não são originadas no organismo, mas sim em fatores externos, como acidentes e violências.''',
            style={'text-align': 'justify', 'color': 'white'})
        ])


    return desc_base, desc_sub_base

# Atualiza Tabela e gráficos
@callback(
    Output(component_id='data_table', component_property='data'),
    Output(component_id='registros_base', component_property='children'),
    Output(component_id='anos_base', component_property='children'),
    Output(component_id='explorar', component_property='children'),
    Input(component_id='bases', component_property='value'),
    Input(component_id='dataset', component_property='value')
)
def data_table(base_chosen, table):

    df = dataset[base_chosen][table]

    tam = html.P(f'A base possui {len(df)} registros', style={'text-align': 'center'})

    anos = list(df['DATA'].apply(lambda x: str(x)[:4]).unique())
    range_anos = html.P(f'Os anos variam entre {min(anos)}-{max(anos)}', style={'text-align': 'center'})

    tab = df.head().to_dict('records')
    
    grafico = None
    if table == 'DOEXT':
        grafico = return_simdoext(df)
    elif table == 'DOMAT':
        grafico = return_simdomat(df)
    elif table == 'ZIKA':
        grafico = return_sinanzika(df)
    elif table == 'VIOL':
        grafico = return_sinanviol(df)
    elif table == 'DOFET':
        grafico = return_simdofet(df)

    return tab, tam, range_anos, grafico
