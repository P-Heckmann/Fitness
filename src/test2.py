import gpxpy
import pandas as pd
from geopandas import GeoDataFrame as gdf
from shapely.geometry import Point
from datetime import datetime

# Load activity
act_path = r"C:\Users\paulh\Desktop\Fitness\data\Single_runs\activity_10981175453.csv"

act_df = pd.read_csv(act_path)


# Load gpx.
gpx_path = r"C:\Users\paulh\Desktop\Fitness\data\Geo\activity_10981175453.gpx"

with open(gpx_path) as f:
    gpx = gpxpy.parse(f)

# Convert to a dataframe one point at a time.
points = []
for segment in gpx.tracks[0].segments:
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


long = df.longitude
lat = df.latitude

geometry = [Point(xy) for xy in zip(long, lat)]

df = df.drop(["longitude", "latitude"], axis=1)

df["geometry"] = geometry

# f["time"] = pd.to_datetime(df["time"])


df_geo = gdf(df, crs="EPSG:4326", geometry=geometry)


# convert the timestamp column to datetime
# df['time'] = pd.to_datetime(df['time'])

# calculate the time difference between consecutive rows and add it to a new column called 'time_diff'
df_geo["time_diff"] = df_geo["time"].diff()


df_geo


# df_geo = df_geo.drop(["time", "elevation","time_diff"], axis=1)

# calculate the distance between all pairs of geometries
df_geo["distance"] = df_geo["geometry"].apply(lambda x: df_geo["geometry"].distance(x))


# Use 'GeoSeries.to_crs()' to re-project geometries to a projected CRS before this operation.

df_geo["mean_distance"] = (
    df_geo["geometry"].apply(lambda x: df_geo["geometry"].distance(x)).mean(axis=1)
)

df_geo

x = df_geo.date
y = df_geo.elevation

df_geo.plot(x, y)
