import pandas as pd
import altair as alt
from matplotlib import pyplot as plt
from matplotlib import dates as da
import streamlit as st
import folium
from streamlit_folium import st_folium

# df_gpx = pd.read_pickle(r"./data/gpx-data.pkl")
# df_tcx = pd.read_pickle(r"./data/tcx-data.pkl")
# df_general_tcx = pd.read_pickle(r"./data/general-tcx-data.pkl")

df_gpx = pd.read_pickle(r"C:\Users\paulh\Desktop\Fitness\data\gpx-data.pkl")
df_tcx = pd.read_pickle(r"C:\Users\paulh\Desktop\Fitness\data\tcx-data.pkl")
df_general_tcx = pd.read_pickle(
    r"C:\Users\paulh\Desktop\Fitness\data\general-tcx-data.pkl"
)

TOTAL_DISTANCE = df_general_tcx["DistanceMeters"].sum()
TOTAL_TIME = df_general_tcx["TotalTimeSeconds"].sum()
TOTAL_CALORIES = df_general_tcx["Calories"].sum()

st.write("### Name of Run")
st.markdown("""---""")
st.write(f"#### Distance: {TOTAL_DISTANCE}")
st.write(f"#### Time: {TOTAL_TIME}s")
st.write(f"#### Calories: {TOTAL_CALORIES}")
st.markdown("""---""")

# AVG_PACE = 0
# TOTAL_ASCENT = df_general_tcx["TotalTimeSeconds"].sum

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
    folium.Marker(
        [row["Position.LatitudeDegrees"], row["Position.LongitudeDegrees"]],
        icon=folium.Icon(color="blue", icon="flag", prefix=""),
    ).add_to(m)

# call to render Folium map in Streamlit
st_data = st_folium(m, width=700, height=400)

st.markdown("""---""")

chart = (
    (
        alt.Chart(df_tcx)
        .mark_point()
        .encode(
            x=alt.X("DistanceMeters", scale=alt.Scale(zero=False)),
            y=alt.Y("AltitudeMeters", scale=alt.Scale(zero=False)),
        )
    )
    .properties(width=700, height=400)
    .interactive()
)

chart

st.markdown("""---""")

# Define the chart
chart = (
    alt.Chart(df_tcx)
    .mark_point()
    .encode(
        x=alt.X("Time:T", axis=alt.Axis(format="%H:%M")),
        y=alt.Y("AltitudeMeters", scale=alt.Scale(zero=False)),
    )
    .properties(width=700, height=400)
    .interactive()
)

chart
