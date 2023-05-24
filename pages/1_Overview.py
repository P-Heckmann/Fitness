import streamlit as st
import gpxpy
import pandas as pd
from geopandas import GeoDataFrame as gdf
from shapely.geometry import Point
from datetime import datetime

st.write("# Welcome to Fitness-tracker")


# Load activity
act_path = r"C:\Users\paulh\Desktop\Fitness\data\Single_runs\activity_10981175453.csv"

act_df = pd.read_csv(act_path)

st.dataframe(act_df)  # Same as st.write(df)
