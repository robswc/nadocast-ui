import dash
from dash import dcc

dash.register_page(__name__, path_template="/map", name="Map")


def layout():
    return dcc.Location(pathname="/map/today", refresh=True, id="redirect")
