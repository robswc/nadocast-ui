import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

available_pages = dash.page_registry.values()
# available_pages = [page for page in available_pages if page["name"] != "Home"]
available_pages = [page for page in available_pages if page["name"] != "Map"]

app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Data", href="/data")),
            dbc.NavItem(dbc.NavLink("Map", href="/map")),
        ],
        brand=html.Img(
            src="/assets/nadocast-ui-logo.png", height=64,
        ),
        brand_href="/",
        color="black",
        dark=True,
        className='mb-3'
    ),
    dash.page_container
])

server = app.server

if __name__ == '__main__':
    app.run(debug=True)
