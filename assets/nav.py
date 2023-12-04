import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output


menu_style = {
    'background-color': '#1B263B',  
    'border-radius': '10px',
    'padding': '10px',
    'color': '#FFFFFF'
}


default_style = {
    'background-color': '#415A77',  
    'border-radius': '10px', 
    'padding': '10px',
    'color': '#FFFFFF'
}


_nav = dbc.Container([
	dbc.Row([dbc.Col([html.H1(['Análise Temporal Datasus'], className='app-brand', style={'margin-top': 25, 'margin-bottom': 15, 'color': 'white'})], width = 3)
	]),
	dbc.Row([
        dbc.Col([
                dbc.Nav(
                [
                    dbc.NavLink(html.Img(src='https://github.com/EduardoDuX/Datasus-Timeseries/blob/main/assets/Icons/vetor_home.png?raw=true'), id='home_button'),
                    dbc.NavLink(html.Img(src='https://github.com/EduardoDuX/Datasus-Timeseries/blob/main/assets/Icons/vetor_grafico.png?raw=true'), id='analise_button')
                    ],
                    vertical=True, pills=True, class_name='my-nav', horizontal='start')
                ], width = 3),

        dbc.Col(
            html.Div(style={'width': '1px', 'background-color': 'black', 'height': '100%', 'margin-left': '13px'}),
            width = 1
        ),

        dbc.Col(
                id = 'sub_menu', width = 4, align='center'
                )
    ], style = default_style)
        
    ]
)

@callback(
    Output(component_id='sub_menu', component_property='children'),
    Output(component_id='home_button', component_property='style'),
    Output(component_id='analise_button', component_property='style'),
    Input(component_id='home_button', component_property='n_clicks_timestamp'),
    Input(component_id='analise_button', component_property='n_clicks_timestamp')

)
def secondary_menu(n_clicks_timestamp1, n_clicks_timestamp2):    
    if n_clicks_timestamp1 == None and n_clicks_timestamp2 == None:
        menu = html.Div()
        home = default_style
        data = default_style
    
    elif (n_clicks_timestamp1 != None and n_clicks_timestamp2 == None) or (n_clicks_timestamp1 != None and n_clicks_timestamp1 > n_clicks_timestamp2):
        menu = dbc.Nav(
                [
                    dbc.NavLink('Home', href='/', style= default_style, id= 'home'),
                    dbc.NavLink('Dados', href='/dados', style= default_style, id= 'dados')
                ],
                vertical=True, pills=True, class_name='my-nav2', horizontal='center')
        home = menu_style
        data = default_style
    else:
        menu = dbc.Nav(
                [
                    dbc.NavLink('Exploração', href='/exploracao', style= default_style, id= 'exploracao'),
                    # dbc.NavLink('Correlações', href='/correlacao', style= default_style, id= 'correlacoes'),
                    dbc.NavLink('Estimação', href='/estimacao', style= default_style, id= 'estimacao'),
                    dbc.NavLink('Diagnóstico', href='/diagnostico', style= default_style, id= 'diagnostico'),
                    dbc.NavLink('Predição', href='/predicao', style= default_style, id= 'predicao')
                ],
                vertical=True, pills=True, class_name='my-nav3', horizontal='center')
        data = menu_style
        home = default_style

    return menu, home, data

@callback(
    Output(component_id='home', component_property='style'),
    Output(component_id='dados', component_property='style'),
    Input(component_id='home', component_property='n_clicks_timestamp'),
    Input(component_id='dados', component_property='n_clicks_timestamp'),
)

def style_home_adjust(home = None, dados = None):
    timestamps = {
        'home': home,
        'dados': dados,
    }
    
    styles = {
        'home': default_style,
        'dados': default_style,
    }
    for times in timestamps.keys():
        if timestamps[times] == None:
            timestamps[times] = 0

    val = max(timestamps.values())
    key = list(timestamps.keys())[list(timestamps.values()).index(val)]
    
    if val > 0:
        styles[key] = menu_style
    return styles['home'], styles['dados']
    

@callback(
    Output(component_id='exploracao', component_property='style'),
    # Output(component_id='correlacoes', component_property='style'),
    Output(component_id='estimacao', component_property='style'),
    Output(component_id='diagnostico', component_property='style'),
    Output(component_id='predicao', component_property='style'),
    Input(component_id='exploracao', component_property='n_clicks_timestamp'),
    # Input(component_id='correlacoes', component_property='n_clicks_timestamp'),
    Input(component_id='modelagem', component_property='n_clicks_timestamp'),
    Input(component_id='diagnostico', component_property='n_clicks_timestamp'),
    Input(component_id='predicao', component_property='n_clicks_timestamp')
)

def style_analise_adjust(exploracao = None, correlacoes = None, estimacao = None, diagnostico = None, predicao = None):

    timestamps = {
        'exploracao': exploracao,
        # 'correlacoes': correlacoes,
        'estimacao': estimacao,
        'diagnostico': diagnostico,
        'predicao': predicao
    }
    
    styles = {
        'exploracao': default_style,
        # 'correlacoes': default_style,
        'modelagem': default_style,
        'diagnostico': default_style,
        'predicao': default_style
    }
    
    for times in timestamps.keys():
        if timestamps[times] == None:
            timestamps[times] = 0

    val = max(timestamps.values())
    key = list(timestamps.keys())[list(timestamps.values()).index(val)]
    
    if val > 0:
        styles[key] = menu_style
    return styles['exploracao'], styles['modelagem'], styles['diagnostico'], styles['predicao']
    