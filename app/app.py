import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Img(
        src="https://private-user-images.githubusercontent.com/38849824/328594107-086804c2-79ec-41bf-b2c1"
            "-b5e704a72b2d.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTUxMTY3MzgsIm5iZiI6MTcxNTExNjQzOCwicGF0aCI6Ii8zODg0OTgyNC8zMjg1OTQxMDctMDg2ODA0YzItNzllYy00MWJmLWIyYzEtYjVlNzA0YTcyYjJkLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA1MDclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNTA3VDIxMTM1OFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTkxMzJlYzA3OWVkYjlmMzRiZmMwMmY5NjdkN2UzZGRmOGEwZTY5ZmFjNTJhYjRkNDRlZDJiZjczODk5MThiM2MmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.sCIAi1TEOcYqanRaThPF4JJ70AmeRAcH0tBMAPV5aCI",
        height=64,
    ),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])

server = app.server

if __name__ == '__main__':
    app.run(debug=True)
