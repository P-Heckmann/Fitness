import folium
import json
from streamlit_folium import st_folium
from pathlib import Path
import os

path = Path(r"C:\Users\paulh\Desktop\Fitness\data\map.geojson")
# path = Path(r"./data/map.geojson")

county_geojson = json.load(open(path))

first_coordinates = county_geojson["features"][0]["geometry"]["coordinates"]

m = folium.Map(
    location=(first_coordinates[1], first_coordinates[0]),
    zoom_start=15,
    tiles="cartodb positron",
)

folium.GeoJson(data=county_geojson).add_to(m)


# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)
