import os
from datetime import datetime

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dash_table
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
from dash.html import H2
from plotly.graph_objs import Figure
from utils import ui
from utils.data import create_probabilities_df
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


def map_card():

    return ui.card(
        title=html.H2(id="title"),
        children=dcc.Loading(
            dcc.Graph(
                id="map",
                figure={},
                config={"scrollZoom": True},
                responsive=True,
                style={"height": "60vh"},
            )
        ),
    )


def table_card():

    return ui.card(
        title="County and Tornado Probability",
        children=dcc.Loading(
            dash_table.DataTable(
                id="table",
                data=[],
                columns=[{"name": i, "id": i} for i in ["name", "tornado_probability"]],
                editable=False,
                filter_action="native",
                sort_action="native",
                page_size=20,
                style_data={
                    "width": "150px",
                    "minWidth": "150px",
                    "maxWidth": "150px",
                    "overflow": "hidden",
                    "textOverflow": "ellipsis",
                },
            )
        ),
    )


def layout(filename: str | None = None, **kwargs):

    return html.Div(
        [
            dcc.Input(id="filename", value=filename, type="hidden"),
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [map_card()],
                                xs=12,
                                sm=12,
                                md=6,
                                lg=6,
                                xl=6,
                                xxl=6,
                            ),
                            dbc.Col(
                                table_card(),
                                xs=12,
                                sm=12,
                                md=6,
                                lg=6,
                                xl=6,
                                xxl=6,
                            ),
                        ],
                        className="mb-3",
                    )
                ],
                fluid=True,
            ),
        ]
    )


@callback(
    Output("title", "children"),
    Output("map", "figure"),
    Output("table", "data"),
    # add an input that triggers on page load
    Input("filename", "value"),
)
def update_map(filename: str) -> tuple[str, Figure, list[dict]]:

    def get_datetime_from_path(file_path: str):
        # get just the filename
        fname = file_path.split("/")[-1]
        # remove the extension
        fname = fname.split(".")[0]
        # remove the hour
        fname = fname.split("_")[0]
        day = fname[-2:]
        month = fname[-4:-2]
        year = fname[:-4]
        return datetime(int(year), int(month), int(day))

    if filename == "today" or filename is None:
        # Define constant for directory path
        PROBABILITY_DIR = "storage/fips_probabilities"

        def get_forecast_date_and_path(date_str):
            """Returns the forecast date and path based on the given date string."""
            forecast_dt = datetime.strptime(date_str, "%Y%m%d")
            path = f"{PROBABILITY_DIR}/{date_str}_0.csv"
            return forecast_dt, path

        def get_or_create_forecast(date_str):
            """Returns the forecast date and path, creating the forecast if necessary."""
            if date_str in all_files:
                return get_forecast_date_and_path(date_str)
            else:
                forecast_dt = datetime.now()
                create_probabilities_df(date=forecast_dt, hour=0, day=1)
                return (
                    forecast_dt,
                    f"{PROBABILITY_DIR}/{forecast_dt.strftime('%Y%m%d')}_0.csv",
                )

        # Get all files, excluding ".keep" and removing the hour
        all_files = [
            f.split("_")[0] for f in os.listdir(PROBABILITY_DIR) if f != ".keep"
        ]

        # Get or create forecast for today
        today = datetime.now().strftime("%Y%m%d")
        forecast_dt, path = get_or_create_forecast(today)

    else:
        path = f"storage/fips_probabilities/{filename}.csv"
        forecast_dt = get_datetime_from_path(path)

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

    title = f"Forecast for {forecast_dt.strftime('%Y-%m-%d')}"

    return title, fig, df.to_dict("records")
