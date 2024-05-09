import datetime

import dash
from dash import html, callback, Input, Output

from utils.data import (
    create_probabilities_df,
    list_forecasts,
)
from utils.ui import input_group
import dash_bootstrap_components as dbc

dash.register_page(__name__)

TZ_OPTIONS = [
    {"label": "0z", "value": 0},
    {"label": "12z", "value": 12},
    {"label": "14z", "value": 14},
]

layout = dbc.Container(
    [
        html.H1("Get Forecast"),
        input_group(
            component_id="date",
            label="Date",
            value=datetime.datetime.now(),
            input_type="date",
        ),
        input_group(
            component_id="hour",
            label="Hour",
            value=0,
            input_type="dropdown",
            options=TZ_OPTIONS,
        ),
        dbc.Button("Get Forecast", id="get-forecast", className="w-100"),
        html.Div(id="forecast-output"),
        html.H1("All Forecasts"),
        html.Div(id="all-forecasts"),
        dbc.Button("Refresh", id="get-all-forecasts", className="w-100"),
    ]
)


@callback(
    Output("forecast-output", "children"),
    Input("get-forecast", "n_clicks"),
    Input("date", "date"),
    Input("hour", "value"),
)
def get_forecast(n_clicks, date: str, hour: int):
    if n_clicks is None:
        return ""

    # get a datetime object from date string, it will come in like this '2024-05-07T15:34:23.565221'
    created_datetime = datetime.datetime.strptime(date.split("T")[0], "%Y-%m-%d")
    print(f"Selected Date {created_datetime} Hour {hour}")

    create_probabilities_df(created_datetime, hour, 1)

    return "Downloaded forecast"


@callback(
    Output("all-forecasts", "children"),
    Input("get-all-forecasts", "n_clicks"),
)
def get_all_forecasts(n_clicks):
    forecast_files = list_forecasts(path="storage/fips_probabilities", recursive=True)
    forecasts = []
    for f in forecast_files:
        forecasts.append(
            html.Tr(
                [
                    html.Td(f),
                    html.Td(
                        dbc.Button(
                            "View", href=f"/map/{f.split('/')[-1].split('.')[0]}"
                        )
                    ),
                ],
                className="d-flex justify-content-between align-items-center",
            )
        )
    return html.Table(forecasts)
