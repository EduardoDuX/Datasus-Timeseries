from dash import html
import dash_bootstrap_components as dbc

_footer = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([html.Hr([], className = 'hr-footer')], width = 12)
        ]),
        dbc.Row([
	        dbc.Col([], width = 1),
            dbc.Col(['Created with Plotly Dash'], width = 3),
            dbc.Col([], width =6),
	        dbc.Col([
                html.Ul([
                    html.Li([
                        html.A([ html.I(className="fa-brands fa-github me-3 fa-1x")], href='https://github.com/EduardoDuX/Datasus-Timeseries'),
                        html.A([ html.Img(src='https://github.com/EduardoDuX/Datasus-Timeseries/blob/main/usp-logo-transparente-800-400.png?raw=true',)], href='https://uspdigital.usp.br/jupiterweb/obterDisciplina?nomdis=&sgldis=SME0808'),
                    ])
                ], className='list-unstyled d-flex justify-content-center justify-content-md-start')
            ], width = 2)
        ])
    ], fluid=True)
], className = 'footer')
