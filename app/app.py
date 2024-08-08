import os

import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

available_pages = dash.page_registry.values()
# available_pages = [page for page in available_pages if page["name"] != "Home"]
available_pages = [page for page in available_pages if page["name"] != "Map"]

app.layout = html.Div(
    [
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/")),
                dbc.NavItem(dbc.NavLink("Data", href="/data")),
                dbc.NavItem(dbc.NavLink("Map", href="/map")),
            ],
            brand=html.Img(
                src="/assets/nadocast-ui-logo.png",
                height=48,
            ),
            brand_href="/",
            color="black",
            dark=True,
            className="mb-3",
        ),
        dash.page_container,
        html.Footer(
            [
                html.A(
                    "Source",
                    href="https://github.com/robswc/nadocast-ui",
                    className="text-white",
                ),
                html.A(
                    f"Release: " f"{os.getenv('APP_VERSION', None)}",
                    href=f"https://github.com/robswc/nadocast-ui/releases/tag/{os.getenv('APP_VERSION', None)}",
                    className="text-white",
                ),
            ],
            className="bg-black text-white d-flex align-items-center justify-content-between p-3 mt-3 fixed-bottom",
        ),
    ]
)

server = app.server

if __name__ == "__main__":
    app.run(debug=True)
