import streamlit as st
import pandas as pd
import altair as alt
from matplotlib import pyplot as plt
from matplotlib import dates as da
import streamlit as st
import folium
from streamlit_folium import st_folium
import datetime
import calendar

st.write("# Overview")

# df_gpx = pd.read_pickle(r"./data/gpx-data.pkl")
# df_tcx = pd.read_pickle(r"./data/tcx-data.pkl")
# df_general_tcx = pd.read_pickle(r"./data/general-tcx-data.pkl")


df_tcx = pd.read_pickle(r"C:\Users\paulh\Desktop\Fitness\data\merged-tcx-data.pkl")
df_general_tcx = pd.read_pickle(
    r"C:\Users\paulh\Desktop\Fitness\data\merged-general-tcx-data.pkl"
)

column_mapping1 = {
    "DistanceMeters": "Distance in m",
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

TOTAL_DISTANCE = round(df_general_tcx["Distance"].sum())

TOTAL_TIME_SECONDS = round(df_general_tcx["Time"].sum())
TOTAL_TIME = str(datetime.timedelta(seconds=TOTAL_TIME_SECONDS))

AVG_PACE_SECONDS = TOTAL_TIME_SECONDS / (TOTAL_DISTANCE / 1000)
AVG_PACE = str(datetime.timedelta(seconds=round(AVG_PACE_SECONDS)))

# TOTAL_ASCENT = df_general_tcx["TotalTimeSeconds"].sum
# altitude is in tcx maybe difference betweeen min and max for each run
# and then the sum

TOTAL_CALORIES = df_general_tcx["Calories"].sum()

st.write(f"#### Distance: {TOTAL_DISTANCE} m")
st.write(f"#### Time: {TOTAL_TIME}")
st.write(f"#### Avg Pace: {AVG_PACE} /km")
# st.write(f"#### Total Ascent: {TOTAL_ASCENT}")
st.write(f"#### Calories: {TOTAL_CALORIES}")
st.markdown("""---""")


distance_by_day = df_general_tcx.groupby(df_general_tcx["@StartTime"].dt.date)[
    "Distance"
].sum()

time_by_day = df_general_tcx.groupby(df_general_tcx["@StartTime"].dt.date)["Time"].sum()

# time_by_day = round(time_by_day)


max_pace_by_day = df_general_tcx.groupby(df_general_tcx["@StartTime"].dt.date)[
    "Max Pace"
].max()
calories_by_day = df_general_tcx.groupby(df_general_tcx["@StartTime"].dt.date)[
    "Calories"
].sum()
heart_rate_by_day = df_general_tcx.groupby(df_general_tcx["@StartTime"].dt.date)[
    "Max HR"
].max()


# Create dictionary with series
data = {
    "Distance (m)": distance_by_day,
    "Time (s)": time_by_day,
    "Max Pace (time/km)": max_pace_by_day,
    "Calories": calories_by_day,
    "Heart rate (bpm)": heart_rate_by_day,
}

# Create DataFrame
df = pd.DataFrame(data)
df = df.reset_index()
df["@StartTime"] = df["@StartTime"].astype(str)


variable_names = [
    "Distance (m)",
    "Time (s)",
    "Max Pace (time/km)",
    "Calories",
    "Heart rate (bpm)",
]

selected_variable = st.selectbox(
    "Select a variable to plot", variable_names, index=0, key="1"
)

histogram = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("@StartTime:T", axis=alt.Axis(title="")),
        y=alt.Y(selected_variable),
    )
    .properties(width=700, height=200)
    .interactive()
)
histogram
st.markdown("""---""")

distance_by_month = df_general_tcx.groupby(df_general_tcx["@StartTime"].dt.month)[
    "Distance"
].sum()

time_by_month = df_general_tcx.groupby(df_general_tcx["@StartTime"].dt.month)[
    "Time"
].sum()

max_pace_by_month = df_general_tcx.groupby(df_general_tcx["@StartTime"].dt.month)[
    "Max Pace"
].max()
calories_by_month = df_general_tcx.groupby(df_general_tcx["@StartTime"].dt.month)[
    "Calories"
].sum()
heart_rate_by_month = df_general_tcx.groupby(df_general_tcx["@StartTime"].dt.month)[
    "Max HR"
].max()


# Create dictionary with series
data = {
    "Distance (m)": distance_by_month,
    "Time (s)": time_by_month,
    "Max Pace (time/km)": max_pace_by_month,
    "Calories": calories_by_month,
    "Heart rate (bpm)": heart_rate_by_month,
}

# Create DataFrame
df = pd.DataFrame(data)
df = df.reset_index()

df["@StartTime"] = df["@StartTime"].apply(lambda x: calendar.month_name[x])


selected_variable = st.selectbox(
    "Select a variable to plot", variable_names, index=0, key="2"
)

histogram = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("@StartTime:N", axis=alt.Axis(title="")),
        y=alt.Y(selected_variable),
    )
    .properties(width=700, height=200)
    .interactive()
)
histogram
st.markdown("""---""")
