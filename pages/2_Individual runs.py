import pandas as pd
import altair as alt
from matplotlib import pyplot as plt
from matplotlib import dates as da
import streamlit as st
import folium
from streamlit_folium import st_folium
import datetime


df_tcx = pd.read_pickle(r"./data/merged-tcx-data.pkl")
df_general_tcx = pd.read_pickle(r"./data/merged-general-tcx-data.pkl")


# df_tcx = pd.read_pickle(r"C:\Users\paulh\Desktop\Fitness\data\merged-tcx-data.pkl")
# df_general_tcx = pd.read_pickle(
#    r"C:\Users\paulh\Desktop\Fitness\data\merged-general-tcx-data.pkl"
# )

st.write("# Individual runs")


column_mapping1 = {
    "DistanceMeters": "Distance (m)",
    "Extensions.ns3:TPX.ns3:Speed": "speed",
    "HeartRateBpm.Value": "Heart rate (bpm)",
    "Extensions.ns3:TPX.ns3:RunCadence": "Cadence (spm)",
    "Position.LatitudeDegrees": "Latitude",
    "Position.LongitudeDegrees": "Longitude",
    "AltitudeMeters": "Altitude (m)",
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


df_tcx["Time (minutes)"] = (
    df_tcx["Time"] - df_tcx["Time"].min()
).dt.total_seconds() / 60


df_tcx["date"] = df_tcx["Time"].dt.date

# Get unique dates
unique_dates = df_tcx["date"].unique().tolist()


selected_date = st.selectbox("Select a date", unique_dates, index=0, key="3")


# df_tcx = df_tcx[df_tcx["date"] == datetime.date(2023, 2, 15)]
df_tcx = df_tcx[df_tcx["date"] == selected_date]


TOTAL_DISTANCE = round(df_tcx["Distance (m)"].max())

TOTAL_TIME = round(df_tcx["Time (minutes)"].max())

st.write(f"#### Distance: {TOTAL_DISTANCE} m")
st.write(f"#### Time: {TOTAL_TIME}")


LOCATION = (
    df_tcx["Latitude"][df_tcx.index[1]],
    df_tcx["Longitude"][df_tcx.index[1]],
)


m = folium.Map(
    location=LOCATION,
    zoom_start=15,
    tiles="cartodb positron",
)

for index, row in df_tcx.iterrows():
    folium.CircleMarker([row["Latitude"], row["Longitude"]], radius=1).add_to(m)

folium.Marker(
    location=LOCATION,
    icon=folium.Icon(color="lightgray", icon="Flag", prefix=""),
).add_to(m)


# call to render Folium map in Streamlit
st_data = st_folium(m, width=700, height=400)

st.markdown("""---""")


st.write(f"#### Elevation")

variable_names = ["Time (minutes)", "Distance (m)"]

selected_variable = st.selectbox(
    "Select a variable to plot", variable_names, index=0, key="4"
)

chart = (
    alt.Chart(df_tcx)
    .mark_area()
    .encode(
        x=alt.X(selected_variable),
        y=alt.Y("Altitude (m)", scale=alt.Scale(domain=[0, 300]), title="meters"),
    )
    .interactive()
)

st.altair_chart(chart, use_container_width=True)


st.markdown("""---""")

st.write(f"#### Pace")


selected_variable = st.selectbox(
    "Select a variable to plot", variable_names, index=0, key="5"
)

chart = (
    alt.Chart(df_tcx)
    .mark_area()
    .encode(
        x=alt.X(selected_variable),
        y=alt.Y("speed", scale=alt.Scale(domain=[0, 10]), title="minutes per km"),
    )
    .interactive()
)

st.altair_chart(chart, use_container_width=True)


st.markdown("""---""")

st.write(f"#### Heart rate")


selected_variable = st.selectbox(
    "Select a variable to plot", variable_names, index=0, key="6"
)

chart = (
    alt.Chart(df_tcx)
    .mark_area()
    .encode(
        x=alt.X(selected_variable),
        y=alt.Y("Heart rate (bpm)", scale=alt.Scale(domain=[120, 180]), title="bpm"),
    )
    .interactive()
)

st.altair_chart(chart, use_container_width=True)

st.markdown("""---""")

st.write(f"#### Cadence")


selected_variable = st.selectbox(
    "Select a variable to plot", variable_names, index=0, key="7"
)

chart = (
    alt.Chart(df_tcx)
    .mark_area()
    .encode(
        x=alt.X(selected_variable),
        y=alt.Y("Cadence (spm)", scale=alt.Scale(domain=[50, 100]), title="spm"),
    )
    .interactive()
)

st.altair_chart(chart, use_container_width=True)

st.markdown("""---""")

st.write(f"#### Trainings zone")

ranges = {
    "Zone 1": (0, 112),
    "Zone 2": (113, 131),
    "Zone 3": (132, 149),
    "Zone 4": (150, 168),
    "Zone 5": (169, 300),
}

total_values = len(df_tcx)
percentages = {}

for range_name, (start, end) in ranges.items():
    count = (
        (df_tcx["Heart rate (bpm)"] >= start) & (df_tcx["Heart rate (bpm)"] <= end)
    ).sum()
    percentage = (count / total_values) * 100
    percentages[range_name] = percentage

# Print the percentages
for range_name, percentage in percentages.items():
    print(f"{range_name}: {percentage}%")


# Create a new DataFrame with percentages
percentages_df = pd.DataFrame(percentages, index=["Percentage"])

percentages_df = percentages_df.reset_index()

df_long = pd.melt(
    percentages_df, id_vars="index", var_name="Zone", value_name="Percentage"
)

SUM_TIME = df_tcx["Time (minutes)"].max()

df_long["Time"] = (df_long["Percentage"] / 100) * SUM_TIME


metric_name = ["Percentage", "Time (minutes)"]

selected_variable = st.selectbox(
    "Select a variable to plot", metric_name, index=0, key="8"
)

histogram = (
    alt.Chart(df_long)
    .mark_bar()
    .encode(
        x=alt.X("Zone", axis=alt.Axis(title="")),
        y=alt.Y(selected_variable),
    )
    .interactive()
)

st.altair_chart(histogram, use_container_width=True)
