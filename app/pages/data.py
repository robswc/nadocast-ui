import datetime

import dash
from dash import html, dcc, callback, Input, Output

from utils.data import get_forecasts, download_forecast, create_probabilities_df, list_forecasts

dash.register_page(__name__)

TZ_OPTIONS = [
    {
        'label': '0z',
        'value': 0},
    {
        'label': '12z',
        'value': 12},
    {
        'label': '14z',
        'value': 14},
]

layout = html.Div([
    html.H1('Get Forecast'),
    dcc.DatePickerSingle(
        id='date',
        date=datetime.datetime.now(),
    ),
    dcc.Dropdown(
        id='hour',
        options=TZ_OPTIONS,
        value=0,
    ),
    html.Button('Get Forecast', id='get-forecast'),
    html.Div(id='forecast-output'),
    html.H1("All Forecasts"),
    html.Button('Get All Forecasts', id='get-all-forecasts'),
    html.Div(id='all-forecasts'),
])


@callback(
    Output('forecast-output', 'children'),
    Input('get-forecast', 'n_clicks'),
    Input('date', 'date'),
    Input('hour', 'value'),
)
def get_forecast(n_clicks, date: str, hour: int):
    if n_clicks is None:
        return ''

    # get a datetime object from date string, it will come in like this '2024-05-07T15:34:23.565221'
    date = datetime.datetime.strptime(date.split('T')[0], '%Y-%m-%d')

    probas = create_probabilities_df(date, hour, 1)

    return f"Downloaded forecast"


@callback(
    Output('all-forecasts', 'children'),
    Input('get-all-forecasts', 'n_clicks'),
)
def get_all_forecasts(n_clicks):
    forecast_files = list_forecasts(path='storage/fips_probabilities', recursive=True)
    return html.Ul([html.Li([html.Div(f), dcc.Link(href=f"/map/{f.split('/')[-1].split('.')[0]}")]) for f in
                    forecast_files])
