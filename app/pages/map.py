import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dash_table
from dash import html, dcc, callback, Input, Output

from utils.geo_data import get_fips_geojson

dash.register_page(__name__, path_template='/map/<filename>', name='Map')


def layout(filename: str = None, **kwargs):
    return html.Div([
        html.H1('Map'),
        dcc.Input(id='filename', value=filename, type='hidden'),
        dbc.Container([
            dbc.Row([
                dbc.Col(
                    [
                        dbc.Row([
                            dbc.Col(dcc.Graph(id='map', figure={}, config={
                                'scrollZoom': True}, responsive=True, restyleData=[]),
                                    width=12),
                            dbc.Col([html.H3("Set Day")], width=12),
                        ])
                    ]
                ),
                dbc.Col(
                    dash_table.DataTable(
                        id='table',
                        data=[],
                        columns=[{
                            'name': i,
                            'id': i} for i in ['name', 'tornado_probability']],
                        editable=False,
                        filter_action='native',
                        sort_action='native',
                        style_data={
                            'width': '150px',
                            'minWidth': '150px',
                            'maxWidth': '150px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                        }
                    )
                )
            ])
        ], fluid=True),

    ])


@callback(
    Output('map', 'figure'),
    Output('table', 'data'),
    # add an input that triggers on page load
    Input('filename', 'value')
)
def update_map(filename: str):
    color_range = {
        0.001: 'lightgray',
        0.01: 'gray',
        0.02: 'green',
        0.03: 'lightgreen',
        0.05: 'brown',
        0.1: 'orange',
        0.15: 'red',
        0.3: 'fuchsia',
        0.5: 'purple',
        0.6: 'teal'
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

    color_scale = convert_color_range_to_plotly(color_range)

    path = f'storage/fips_probabilities/{filename}.csv'
    print(path)
    df = pd.read_csv(path, dtype={
        'fips': str})

    print(df.head(5))

    fig = px.choropleth(
        df,
        geojson=get_fips_geojson(),
        locations='fips',
        color='tornado_probability',
        range_color=(0, 60),
        color_continuous_scale=color_scale,
        scope="usa",
        labels={
            'tp': 'probability'},
        hover_data={
            'fips': False,
            'name': True},
        title='Tornado Probability',
    )
    fig.update_layout(margin={
        "r": 10,
        "t": 10,
        "l": 10,
        "b": 10}
    )

    # remove index from the table
    df = df.drop(columns=['Unnamed: 0', 'fips'])

    # round tornado_probability to 2 decimal places
    df['tornado_probability'] = df['tornado_probability'].round(2)

    return fig, df.to_dict('records')
