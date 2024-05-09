import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

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


def layout():
    return dbc.Container([dbc.Card(dcc.Markdown(get_readme_from_github()), body=True)])
