import dash
from dash import dcc
import dash_bootstrap_components as dbc

from utils import ui

dash.register_page(__name__, path_template="/", name="Home")


def get_readme_from_github():
    import requests

    url = "https://raw.githubusercontent.com/robswc/nadocast-ui/main/README.md"
    response = requests.get(url)

    raw = response.text

    # remove any images within the markdown
    raw = raw.split("\n")
    new_raw = []
    for line in raw:
        if not line.startswith("!["):
            new_raw.append(line)
    raw = "\n".join(new_raw)

    return raw


def cards():
    return dbc.Row(
        [
            dbc.Col(
                ui.card(
                    title="See Today's Forecast",
                    children=dbc.CardLink("View", href="/map/today"),
                ), xs=12, sm=12, md=6, lg=6, xl=6, xxl=6,
            ),
            dbc.Col(
                ui.card(
                    title="See Historical Forecasts",
                    children=dbc.CardLink("View", href="/data"),
                ), xs=12, sm=12, md=6, lg=6, xl=6, xxl=6,
            ),
        ]
    )


def layout():
    return dbc.Container(
        [
            cards(),
            dbc.Row(
                [
                    dbc.Col(
                        [dcc.Markdown(get_readme_from_github())],
                        xs=12,
                        sm=12,
                        md=12,
                        lg=12,
                        xl=12,
                        xxl=12,
                    )
                ],
                className="mb-3",
            ),
        ],
        fluid=False,
    )
