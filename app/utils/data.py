import os
import urllib
from html.parser import HTMLParser
from datetime import datetime

import pandas as pd
import geopandas as gpd

import pygrib
# get the data from the server
import requests

from utils.types import ForecastFile

HOST = "http://data.nadocast.com"


def get_forecasts(date: datetime, hour: int = 0, day: int = 1, name: str = None):
    """Returns a list of all the forecasts for the given date and hour"""

    if name is None:
        name = "nadocast_2022_models_conus_tornado_abs_calib"

    class MyHTMLParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.files = []

        def handle_starttag(self, tag, attrs):
            if tag == 'a':
                for attr in attrs:
                    if attr[0] == 'href' and attr[1].endswith('.grib2'):
                        self.files.append(attr[1])

    def list_files(url):
        try:
            response = urllib.request.urlopen(url)
            html = response.read().decode()
            parser = MyHTMLParser()
            parser.feed(html)
        except Exception as e:
            print(f"Failed to list files at {url}, {e}")
            return []
        return parser.files

    tag1 = date.strftime('%Y%m')
    tag2 = date.strftime('%Y%m%d')
    url = f"{HOST}/{tag1}/{tag2}/t{hour if hour else '0'}z/"
    files = list_files(url)
    # convert to forecast file objects
    forecast_files = []
    for f in files:
        start_hour = int(f.split('_')[-1].split('-')[0][1:])
        end_hour = int(f.split('_')[-1].split('-')[1].split('.')[0])
        forecast_files.append(
            ForecastFile(f.split('/')[-1], f, date, hour, start_hour, end_hour)
        )

    # filter by name
    forecast_files = [f for f in forecast_files if name in f.name]

    day_min = (day * 24) - 24
    day_max = day * 24

    print(f"Filtering ({len(forecast_files)}) by day {day} ({day_min}-{day_max})")
    forecast_files = [f for f in forecast_files if day_min <= f.start_hour <= day_max]

    return forecast_files


def download_forecast(forecast: ForecastFile, to_path: str) -> str:
    """Downloads the forecast from the server, returning the filename"""
    url = f"{HOST}/{forecast.path}"
    response = requests.get(url)
    assert response.status_code == 200, f"Failed to download {url}, status code {response.status_code}"

    filename = forecast.name
    filepath = f"{to_path}/{filename}"
    with open(filepath, 'wb') as f:
        f.write(response.content)
    return filepath


def list_forecasts(path: str, recursive: bool = False):
    """List all the forecasts in the given path"""

    # get all .csv files, recursively if needed
    if recursive:
        files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames if f.endswith('.csv')]
    else:
        files = [f for f in os.listdir(path) if f.endswith('.csv')]
    return files


def get_tornado_probability_df(grib_file: str) -> pd.DataFrame:
    grbs = pygrib.open(grib_file)
    grb = grbs.select(name="Tornado probability")[0]
    data, lats, lons = grb.data()
    df = pd.DataFrame({
        'lat': lats.flatten(),
        'lon': lons.flatten(),
        'tornado_probability': data.flatten()
    })
    grbs.close()
    return df


def create_probabilities_df(date: datetime, hour: int, day: int, name: str = None):
    """Create a pandas DataFrame with the probabilities for each forecast"""
    forecast = get_forecasts(datetime(date.year, date.month, date.day), hour=hour, day=1)[0]
    grib_path = download_forecast(forecast, to_path='storage')
    print('Downloaded forecast:', grib_path)

    tpdf = get_tornado_probability_df(grib_path)
    gdf = gpd.read_file('utils/data/geojson-counties-fips.json')

    # now, let us reduce each geometry to a single point (the centroid)
    gdf['centroid'] = gdf['geometry'].centroid
    gdf['lat'] = gdf['centroid'].y
    gdf['lon'] = gdf['centroid'].x
    tornado_gdf = gpd.GeoDataFrame(tpdf, geometry=gpd.points_from_xy(tpdf.lon, tpdf.lat))

    # Set the geometry of gdf to the centroid column
    gdf.set_geometry('centroid', inplace=True)

    tornado_gdf.crs = gdf.crs
    joined_gdf = gpd.sjoin_nearest(gdf, tornado_gdf)

    # rename id to fips
    joined_gdf.rename(columns={
        'id': 'fips'}, inplace=True)

    proba_file_path = f'storage/fips_probabilities/{date.strftime("%Y%m%d")}_{hour}.csv'

    # convert all column names to lowercase
    joined_gdf.columns = [col.lower() for col in joined_gdf.columns]

    # remove alaska and hawaii, they are not in the tornado probabilities
    # we have to remove them based on "state" id column
    joined_gdf = joined_gdf[joined_gdf['state'] != '02']
    joined_gdf = joined_gdf[joined_gdf['state'] != '15']

    joined_gdf = joined_gdf[['fips', 'name', 'state', 'tornado_probability']]

    joined_gdf.to_csv(proba_file_path)

    # remove the grib file
    os.remove(grib_path)

    return proba_file_path
