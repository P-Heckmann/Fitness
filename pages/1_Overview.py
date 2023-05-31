import streamlit as st
import pandas as pd
import altair as alt
from matplotlib import pyplot as plt
from matplotlib import dates as da
import streamlit as st
import folium
from streamlit_folium import st_folium
import datetime

st.write("# Welcome to Fitness-tracker")

# df_gpx = pd.read_pickle(r"./data/gpx-data.pkl")
# df_tcx = pd.read_pickle(r"./data/tcx-data.pkl")
# df_general_tcx = pd.read_pickle(r"./data/general-tcx-data.pkl")


df_tcx = pd.read_pickle(r"C:\Users\paulh\Desktop\Fitness\data\merged-tcx-data.pkl")
df_general_tcx = pd.read_pickle(
    r"C:\Users\paulh\Desktop\Fitness\data\merged-general-tcx-data.pkl"
)
