import json
import plotly.express as px
from dicts import fips
from functions import extract_coords, calculate_center

def mapping(predictions, state=None, district=None):
    predictions['State FIPS'] = predictions['State FIPS'].astype(str).str.zfill(2)
    predictions['District'] = predictions['District'].astype(str).str.zfill(2)
    predictions['FIPS_CD'] = predictions['State FIPS'] + predictions['District']
    predictions['Dem Advantage'] = predictions['Predicted Democratic %'] - predictions['Predicted Republican %']

    file_path = 'gz_2010_us_500_11_5m.json'
    with open(file_path) as file:
        geo_data = json.load(file)

    for feature in geo_data["features"]:
        if feature["properties"]["CD"] == "00":
            feature["properties"]["CD"] = "01"
        state_cd = feature["properties"]["STATE"] + feature["properties"]["CD"]
        feature["id"] = state_cd

    if state is None and district is None:
        zoom_level = 2
        center_lat = 37.0902
        center_lon = -95.7129
    else:
        state_fips = fips()
        state_names = list(state_fips)
        new_state = state_fips.get(state, "Unknown")
        state = new_state
        district = str(district).zfill(2)
        zoom_level = 6
        center_lat, center_lon = 0, 0
        found = False
        for feature in geo_data["features"]:
            if feature["properties"]["STATE"] == state and feature["properties"]["CD"] == district:
                coords = feature["geometry"]["coordinates"][0]
                center_lat, center_lon = calculate_center(coords)
                found = True
                break
        if not found:
            return "no json"

    fig = px.choropleth_mapbox(predictions, geojson=geo_data, locations='FIPS_CD', color='Dem Advantage',
                               color_continuous_scale="RdBu",
                               range_color=(-50, 50),
                               mapbox_style="carto-positron",
                               color_continuous_midpoint=0,
                               zoom=zoom_level,
                               center={"lat": center_lat, "lon": center_lon},
                               opacity=0.7,
                               labels={'Dem Advantage': 'Predicted Dem Advantage %'},
                               hover_data=['State', 'District', 'Predicted Winner', 'Predicted Democratic %', 'Predicted Republican %'],
                              )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig