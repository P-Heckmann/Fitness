import xml.etree.ElementTree as ET
import xmltodict
import pandas as pd
import os
import glob

file_path = r"C:\Users\paulh\Desktop\Fitness\data\activity_11182302898.tcx"
with open(file_path, "r") as f:
    data = xmltodict.parse(f.read())

# Extract the activity data from the dictionary
activity = data["TrainingCenterDatabase"]["Activities"]["Activity"]

# Conversion to DataFrame
df = pd.json_normalize(activity, record_path=["Lap"])

df = df.drop(["Intensity", "TriggerMethod", "Track.Trackpoint"], axis=1)

cols_to_float = [
    "TotalTimeSeconds",
    "DistanceMeters",
    "MaximumSpeed",
    "Extensions.ns3:LX.ns3:AvgSpeed",
]

cols_to_int = [
    "Calories",
    "AverageHeartRateBpm.Value",
    "MaximumHeartRateBpm.Value",
    "Extensions.ns3:LX.ns3:AvgRunCadence",
    "Extensions.ns3:LX.ns3:MaxRunCadence",
]

# Convert to float
df[cols_to_float] = df[cols_to_float].astype(float)

# Convert to int
df[cols_to_int] = df[cols_to_int].astype(int)

# Convert to datetime
df["@StartTime"] = pd.to_datetime(df["@StartTime"])


df
