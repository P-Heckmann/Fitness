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

column_mapping2 = {
    "TotalTimeSeconds": "Time",
    "DistanceMeters": "Distance",
    "AverageHeartRateBpm.Value": "Avg HR",
    "MaximumHeartRateBpm.Value": "Max HR",
    "MaximumSpeed": "Max Pace",
    "Extensions.ns3:LX.ns3:AvgSpeed": "Avg Pace",
    "Extensions.ns3:LX.ns3:AvgRunCadence": "Avg Cadence",
    "Extensions.ns3:LX.ns3:MaxRunCadence": "Max Cadence",
}
# Rename the columns using the mapping
df_general_tcx = df_general_tcx.rename(columns=column_mapping2)

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

test = df_tcx["Latitude"][0]

m = folium.Map(
    location=(
        df_tcx["Latitude"][0],
        df_tcx["Longitude"][0],
    ),
    zoom_start=15,
    tiles="cartodb positron",
)

for index, row in df_tcx.iterrows():
    folium.CircleMarker([row["Latitude"], row["Longitude"]], radius=1).add_to(m)

folium.Marker(
    location=(
        df_tcx["Latitude"][0],
        df_tcx["Longitude"][0],
    ),
    icon=folium.Icon(color="lightgray", icon="Flag", prefix=""),
).add_to(m)

folium.Marker(
    location=(
        df_tcx["Latitude"][20],
        df_tcx["Longitude"][20],
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


st.write(f"#### Elevation")

variable_names = ["Time", "Distance"]

selected_variable = st.selectbox(
    "Select a variable to plot", variable_names, index=0, key="1"
)

chart = (
    alt.Chart(df_tcx)
    .mark_area()
    .encode(
        x=alt.X(selected_variable),
        y=alt.Y("Altitude", scale=alt.Scale(domain=[0, 300]), title="meters"),
    )
    .properties(width=700, height=200)
    .interactive()
)

chart

st.markdown("""---""")

st.write(f"#### Pace")


selected_variable = st.selectbox(
    "Select a variable to plot", variable_names, index=0, key="2"
)

chart = (
    alt.Chart(df_tcx)
    .mark_area()
    .encode(
        x=alt.X(selected_variable),
        y=alt.Y("speed", scale=alt.Scale(domain=[0, 10]), title="minutes per km"),
    )
    .properties(width=700, height=200)
    .interactive()
)

chart

st.markdown("""---""")

st.write(f"#### Heart rate")


selected_variable = st.selectbox(
    "Select a variable to plot", variable_names, index=0, key="3"
)

chart = (
    alt.Chart(df_tcx)
    .mark_area()
    .encode(
        x=alt.X(selected_variable),
        y=alt.Y("Heart rate", scale=alt.Scale(domain=[120, 180]), title="bpm"),
    )
    .properties(width=700, height=200)
    .interactive()
)

chart

st.markdown("""---""")

st.write(f"#### Cadence")


selected_variable = st.selectbox(
    "Select a variable to plot", variable_names, index=0, key="4"
)

chart = (
    alt.Chart(df_tcx)
    .mark_area()
    .encode(
        x=alt.X(selected_variable),
        y=alt.Y("Cadence", scale=alt.Scale(domain=[50, 100]), title="spm"),
    )
    .properties(width=700, height=200)
    .interactive()
)

chart


st.markdown("""---""")

st.write(f"#### Laps")


df_general_tcx["Lap"] = list(range(1, len(df_general_tcx) + 1))


df_general_tcx["Time"] = df_general_tcx["Time"].astype(int)

df_general_tcx["Distance"] = df_general_tcx["Distance"].astype(int)

# df_general_tcx["Time"] = str(datetime.timedelta(seconds=df_general_tcx["Time"]))

df_general_tcx["Cumulative time"] = df_general_tcx["Time"]

# total ascent
# total descent

# summary

df_laps = df_general_tcx[
    [
        "Lap",
        "Time",
        "Cumulative time",
        "Distance",
        "Avg Pace",
        #        "Max Pace",
        "Avg HR",
        #        "Max HR",
        "Avg Cadence",
        #        "Max Cadence",
        "Calories",
    ]
]

df_laps.loc["Summary"] = df_laps.agg(
    {
        "Time": "sum",
        "Cumulative time": "sum",
        "Distance": "sum",
        "Avg Pace": "mean",
        #        "Max Pace": "mean",
        "Avg HR": "mean",
        #        "Max HR": "mean",
        "Avg Cadence": "mean",
        #        "Max Cadence": "mean",
        "Calories": "mean",
    }
)

st.dataframe(df_laps)


st.markdown("""---""")

st.write(f"#### Heart Rate Zones")

# Create the Altair histogram
