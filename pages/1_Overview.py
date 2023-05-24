import streamlit as st
import pandas as pd


st.write("# Welcome to Fitness-tracker")


# Load activity
act_path = r"C:\Users\paulh\Desktop\Fitness\data\Single_runs\activity_10981175453.csv"

path = r"./data/Single_runs/activity_10981175453.csv"

act_df = pd.read_csv(path)

st.dataframe(act_df)  # Same as st.write(df)
