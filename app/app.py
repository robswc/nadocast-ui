import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

available_pages = dash.page_registry.values()
available_pages = [page for page in available_pages if page["name"] != "Home"]
available_pages = [page for page in available_pages if page["name"] != "Map"]

app.layout = html.Div([
    html.Img(
        src="/assets/nadocast-ui-logo.png", height=64,
    ),
    html.Ul([
        html.Li(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in available_pages
    ]),
    dash.page_container
])

server = app.server

if __name__ == '__main__':
    app.run(debug=True)
