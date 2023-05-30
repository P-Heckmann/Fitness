import pandas as pd
import altair as alt
from matplotlib import pyplot as plt
from matplotlib import dates as da
import streamlit as st
import folium
from streamlit_folium import st_folium
import datetime


# df_gpx = pd.read_pickle(r"./data/gpx-data.pkl")
df_tcx = pd.read_pickle(r"./data/tcx-data.pkl")
df_general_tcx = pd.read_pickle(r"./data/general-tcx-data.pkl")

# df_gpx = pd.read_pickle(r"C:\Users\paulh\Desktop\Fitness\data\gpx-data.pkl")
# df_tcx = pd.read_pickle(r"C:\Users\paulh\Desktop\Fitness\data\tcx-data.pkl")
# df_general_tcx = pd.read_pickle(
#    r"C:\Users\paulh\Desktop\Fitness\data\general-tcx-data.pkl"
# )

TOTAL_DISTANCE = round(df_general_tcx["DistanceMeters"].sum())
TOTAL_TIME_SECONDS = round(df_general_tcx["TotalTimeSeconds"].sum())

TOTAL_TIME = str(datetime.timedelta(seconds=TOTAL_TIME_SECONDS))

AVG_PACE_SECONDS = TOTAL_TIME_SECONDS / (TOTAL_DISTANCE / 1000)
AVG_PACE = str(datetime.timedelta(seconds=round(AVG_PACE_SECONDS)))

# TOTAL_ASCENT = df_general_tcx["TotalTimeSeconds"].sum

TOTAL_CALORIES = df_general_tcx["Calories"].sum()

st.write("### Name and date of Run")
st.markdown("""---""")
st.write(f"#### Distance: {TOTAL_DISTANCE} m")
st.write(f"#### Time: {TOTAL_TIME}")
st.write(f"#### Avg Pace: {AVG_PACE} /km")
# st.write(f"#### Total Ascent: {TOTAL_ASCENT}")
st.write(f"#### Calories: {TOTAL_CALORIES}")
st.markdown("""---""")


# first_coordinates = data["features"][0]["geometry"]["coordinates"]

test = df_tcx["Position.LatitudeDegrees"][0]

m = folium.Map(
    location=(
        df_tcx["Position.LatitudeDegrees"][0],
        df_tcx["Position.LongitudeDegrees"][0],
    ),
    zoom_start=15,
    tiles="cartodb positron",
)

for index, row in df_tcx.iterrows():
    folium.CircleMarker(
        [row["Position.LatitudeDegrees"], row["Position.LongitudeDegrees"]], radius=1
    ).add_to(m)

folium.Marker(
    location=(
        df_tcx["Position.LatitudeDegrees"][0],
        df_tcx["Position.LongitudeDegrees"][0],
    ),
    icon=folium.Icon(color="lightgray", icon="Flag", prefix=""),
).add_to(m)

folium.Marker(
    location=(
        df_tcx["Position.LatitudeDegrees"][20],
        df_tcx["Position.LongitudeDegrees"][20],
    ),
    icon=folium.Icon(color="green", icon="Flag", prefix=""),
).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=700, height=400)

st.markdown("""---""")


# df_gpx["minutes"] = (df_gpx["time"] - df_gpx["time"].min()).dt.total_seconds() / 60
df_tcx["Time"] = (df_tcx["Time"] - df_tcx["Time"].min()).dt.total_seconds() / 60
# df_tcx["Distance in meters"] = df_tcx["DistanceMeters"]
# df_tcx["speed"] = df_tcx["Extensions.ns3:TPX.ns3:Speed"]
# df_tcx["Heart rate"] = df_tcx["HeartRateBpm.Value"]
# df_tcx["Cadence"] = df_tcx["Extensions.ns3:TPX.ns3:RunCadence"]


column_mapping1 = {
    "DistanceMeters": "Distance",
    "Extensions.ns3:TPX.ns3:Speed": "speed",
    "HeartRateBpm.Value": "Heart rate",
    "Extensions.ns3:TPX.ns3:RunCadence": "Cadence",
    "Position.LatitudeDegrees": "Latitude",
    "Position.LongitudeDegrees": "Longitude",
    "AltitudeMeters": "Altitude",
}
# Rename the columns using the mapping
df_tcx = df_tcx.rename(columns=column_mapping1)


st.write(f"#### Elevation")

variable_names = ["Time", "Distance"]

selected_variable = st.selectbox(
    "Select a variable to plot", variable_names, index=0, key="1"
)
