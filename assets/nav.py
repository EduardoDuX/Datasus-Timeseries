import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output


menu_style = {
    'background-color': '#1B263B',  
    'border-radius': '10px',
    'padding': '10px'
}


default_style = {
    'background-color': '#415A77',  
    'border-radius': '10px', 
    'padding': '10px'
}


_nav = dbc.Container([
	dbc.Row([dbc.Col([html.H1(['Análise Temporal Datasus'], className='app-brand', style={'marginTop': 25})], width = 3)
	]),
	dbc.Row([
        dbc.Col([
                dbc.Nav(
                [
                    dbc.NavLink(html.Img(src='https://github.com/ciziks/datasus-analysis/blob/main/assets/Icons/vetor_home.png?raw=true'), id='home_button'),
                    dbc.NavLink(html.Img(src='https://github.com/ciziks/datasus-analysis/blob/main/assets/Icons/vetor_grafico.png?raw=true'), id='analise_button')
                    ],
                    vertical=True, pills=True, class_name='my-nav')
                ], width = 3),
        
        dbc.Col(
                id = 'test', width = 5
                )
    ], style = default_style)
        
])

@callback(
    Output(component_id='test', component_property='children'),
    Output(component_id='home_button', component_property='style'),
    Output(component_id='analise_button', component_property='style'),
    Input(component_id='home_button', component_property='n_clicks_timestamp'),
    Input(component_id='analise_button', component_property='n_clicks_timestamp')

)
def secondary_menu(n_clicks_timestamp1, n_clicks_timestamp2):    
    if n_clicks_timestamp1 is None and n_clicks_timestamp2 is None:
        menu = html.Div()
        home = default_style
        data = default_style
        
    elif (n_clicks_timestamp1 is not None and n_clicks_timestamp2 is None) or n_clicks_timestamp1 > n_clicks_timestamp2:
        menu = dbc.Nav(
                [
                    dbc.NavLink('Home', href='/', style= {'color': '#FFFFFF'}),
                    dbc.NavLink('Dados', href='/dados', style= {'color': '#FFFFFF'})
                ],
                vertical=True, pills=True, class_name='my-nav2')
        home = menu_style
        data = default_style
    else:
        menu = dbc.Nav(
                [
                    dbc.NavLink('Exploração', href='/exploracao', style= {'color': '#FFFFFF'}),
                    dbc.NavLink('Correlações', href='/correlacao', style= {'color': '#FFFFFF'}),
                    dbc.NavLink('Modelagem', href='/modelagem', style= {'color': '#FFFFFF'}),
                    dbc.NavLink('Diagnóstico', href='/diagnostico', style= {'color': '#FFFFFF'}),
                    dbc.NavLink('Predição', href='/predicao', style= {'color': '#FFFFFF'})
                ],
                vertical=True, pills=True, class_name='my-nav3')
        data = menu_style
        home = default_style

    
    return menu, home, data

