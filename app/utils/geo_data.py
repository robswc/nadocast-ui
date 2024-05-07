import json


def get_fips_geojson():
    """Get the FIPS geojson file"""
    fips = json.load(open("utils/data/geojson-counties-fips.json"))
    # filter out the non-continental US
    fips['features'] = [f for f in fips['features'] if f['properties']['STATE'] not in ['02', '15', '72', '78']]
    return fips
