import datetime

import dash
import pandas as pd
from dash import html, callback, Input, Output
from dash.dash_table import DataTable

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
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        html.H1("Generate Forecast"),
                        html.P(
                            "Here we can generate a forecast for a specific date and hour, if it doesn't already "
                            "exist.  You can view all forecasts below."
                        ),
                        html.Div(
                            [
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
                            ],
                            className="d-flex align-items-center justify-content-start w-100",
                        ),
                        dbc.Button("Generate", id="get-forecast", className="w-100"),
                        html.Div(id="forecast-output"),
                    ],
                    body=True,
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        html.H1("All Forecasts"),
                        html.I(
                            "Slide table right to view more columns and 'View' Button",
                            className="text-muted",
                        ),
                        DataTable(
                            id="all-forecasts",
                            columns=[
                                {"name": "Filename", "id": "Filename"},
                                {"name": "Date", "id": "Date"},
                                {"name": "Year", "id": "Year"},
                                {"name": "Month", "id": "Month"},
                                {"name": "Day", "id": "Day"},
                                {"name": "Hour", "id": "Hour"},
                                {
                                    "name": "View",
                                    "id": "View",
                                    "presentation": "markdown",
                                },
                            ],
                            data=[],
                            page_size=50,
                            sort_action="native",
                            filter_action="native",
                            style_data={
                                "width": "150px",
                                "minWidth": "150px",
                                "maxWidth": "150px",
                                "overflow": "hidden",
                                "textOverflow": "ellipsis",
                            },
                            style_table={"overflowX": "auto"},
                        ),
                        dbc.Button(
                            "Refresh", id="get-all-forecasts", className="w-100 mt-3"
                        ),
                    ],
                    body=True,
                )
            ),
            className="mt-3",
        ),
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
    Output("all-forecasts", "data"),
    Input("get-all-forecasts", "n_clicks"),
)
def get_all_forecasts(n_clicks):

    def _get_day(date_str):
        return datetime.datetime.strptime(date_str, "%Y%m%d").day

    def _get_month(date_str):
        return datetime.datetime.strptime(date_str, "%Y%m%d").month

    def _get_year(date_str):
        return datetime.datetime.strptime(date_str, "%Y%m%d").year

    def _get_hour(date_str):
        return int(date_str.split("_")[-1].split(".")[0])

    forecast_files = list_forecasts(path="storage/fips_probabilities", recursive=True)
    # create dataframe
    forecasts = []
    for file in forecast_files:
        forecasts.append(
            {
                "Filename": str(file).split("/")[-1],
                "Date": datetime.datetime.strptime(
                    str(file).split("/")[-1].split("_")[0], "%Y%m%d"
                ),
                "Year": _get_year(str(file).split("/")[-1].split("_")[0]),
                "Month": _get_month(str(file).split("/")[-1].split("_")[0]),
                "Day": _get_day(str(file).split("/")[-1].split("_")[0]),
                "Hour": _get_hour(str(file).split("/")[-1]),
                "View": f"#### [View Map](/map/{file.split('/')[-1].split('.')[0]})",
            }
        )
    df = pd.DataFrame(forecasts)

    # finally, sort by date (newest first)
    df = df.sort_values(by="Date", ascending=False)

    return df.to_dict("records")
