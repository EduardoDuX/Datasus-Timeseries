from dash import Dash
import dash_bootstrap_components as dbc
import dash
from dash import html
from dash_extensions.enrich import DashProxy, ServersideOutputTransform


app = DashProxy(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
	   suppress_callback_exceptions=True, prevent_initial_callbacks=True, transforms=[ServersideOutputTransform()])
server = app.server

# style={'background-color': '#99A3A4'}
# Import shared components
from assets.nav import _nav
from assets.footer import _footer


# App Layout
app.layout = dbc.Container([
	dbc.Row([
        dbc.Col([_nav], width = 2, style={'background-color': '#778DA9'}),
        dbc.Col([
            dbc.Row([dash.page_container])
	    ], width = 10),
    ], style={'height': '100%'}),
    dbc.Row([
        _footer   
    ], style={'height': '10%'})
], fluid=True, style={'background-color':'#E0E1DD','position':'absolute'})


# Run App
if __name__ == '__main__':
	app.run_server(debug=True, host='0.0.0.0')