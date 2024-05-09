import os

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dash_table
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go

from utils.geo_data import get_fips_geojson

dash.register_page(__name__, path_template="/map/<filename>", name="Map")

COLOR_RANGE = {
    0.001: "lightgray",
    0.01: "gray",
    0.02: "green",
    0.03: "lightgreen",
    0.05: "brown",
    0.1: "orange",
    0.15: "red",
    0.3: "fuchsia",
    0.5: "purple",
    0.6: "teal",
}


def convert_color_range_to_plotly(color_range):
    # first, we have to scale the values to 0-1
    max_val = max(color_range.keys())
    min_val = min(color_range.keys())
    color_scale = []
    for i, (val, color) in enumerate(color_range.items()):
        if i == 0:
            color_scale.append((0.0, color))
        elif i == len(color_range) - 1:
            color_scale.append((1.0, color))
        else:
            color_scale.append(((val - min_val) / (max_val - min_val), color))
    return color_scale


COLOR_SCALE = convert_color_range_to_plotly(COLOR_RANGE)


def map():
    return dcc.Graph(
        id="map",
        figure={},
        config={"scrollZoom": True},
        responsive=True,
        style={"height": "60vh"},
    )


def layout(filename: str | None = None, **kwargs):

    return html.Div(
        [
            html.H1("Map"),
            dcc.Input(id="filename", value=filename, type="hidden"),
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [dcc.Loading(map()), html.Div("Parameters")],
                                xs=12,
                                sm=12,
                                md=6,
                                lg=6,
                                xl=6,
                                xxl=6,
                            ),
                            dbc.Col(
                                [
                                    dash_table.DataTable(
                                        id="table",
                                        data=[],
                                        columns=[
                                            {"name": i, "id": i}
                                            for i in ["name", "tornado_probability"]
                                        ],
                                        editable=False,
                                        filter_action="native",
                                        sort_action="native",
                                        style_data={
                                            "width": "150px",
                                            "minWidth": "150px",
                                            "maxWidth": "150px",
                                            "overflow": "hidden",
                                            "textOverflow": "ellipsis",
                                        },
                                    )
                                ],
                                xs=12,
                                sm=12,
                                md=6,
                                lg=6,
                                xl=6,
                                xxl=6,
                            ),
                        ]
                    )
                ],
                fluid=True,
            ),
        ]
    )


@callback(
    Output("map", "figure"),
    Output("table", "data"),
    # add an input that triggers on page load
    Input("filename", "value"),
)
def update_map(filename: str):

    if filename == "today" or filename is None:

        # this needs to be improved later
        all_files = os.listdir("storage/fips_probabilities")
        all_files.remove(".keep")
        # remove the hour
        all_files = [f.split("_")[0] for f in all_files]
        all_files = sorted(all_files)
        latest_file = all_files[-1]
        path = f'storage/fips_probabilities/{latest_file.split(".")[0]}_0.csv'
    else:
        path = f"storage/fips_probabilities/{filename}.csv"

    df = pd.read_csv(path, dtype={"fips": str})

    fig = px.choropleth(
        df,
        geojson=get_fips_geojson(),
        locations="fips",
        color="tornado_probability",
        range_color=(0, 60),
        color_continuous_scale=COLOR_SCALE,
        scope="usa",
        labels={"tp": "probability"},
        hover_data={"fips": False, "name": True},
    )
    fig.update_layout(
        # remove legend
        margin={"r": 10, "t": 0, "l": 10, "b": 0},
        showlegend=False,
        coloraxis=dict(colorbar=dict(orientation="h", y=-0.25)),
    )
    fig.update_geos(fitbounds="locations", visible=False)

    # add cholopleth layer
    fig.add_trace(go.Choropleth())

    # remove index from the table
    df = df.drop(columns=["Unnamed: 0", "fips"])

    # round tornado_probability to 2 decimal places
    df["tornado_probability"] = df["tornado_probability"].round(2)

    return fig, df.to_dict("records")
