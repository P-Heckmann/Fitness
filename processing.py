import gpxpy
import pandas as pd
from pandas_geojson import to_geojson
from pandas_geojson import write_geojson
from geopandas import GeoDataFrame as gdf
from shapely.geometry import Point


# Load activity
act_path = r"./data/Single_runs/activity_10981175453.csv"
act_df = pd.read_csv(act_path)


# Load GPX.
GPX_path = r"./data/Geo/activity_10981175453.gpx"

with open(GPX_path) as f:
    GPX = gpxpy.parse(f)

# Convert to a dataframe one point at a time.
points = []
for segment in GPX.tracks[0].segments:
    for p in segment.points:
        points.append(
            {
                "time": p.time,
                "latitude": p.latitude,
                "longitude": p.longitude,
                "elevation": p.elevation,
            }
        )
        
df = pd.DataFrame.from_records(points)

df['Date'] = df['time'].astype(str)

df


geo_json = to_geojson(df=df, lat='latitude', lon='longitude',
                 properties=['Date','elevation'])

write_geojson(geo_json, filename='map.geojson', indent=4)