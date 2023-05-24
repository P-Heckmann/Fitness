import pandas as pd
import xmltodict
import altair as alt
from matplotlib import pyplot as plt
from matplotlib import dates as da


file = r"C:\Users\paulh\Desktop\Fitness\data\Single_runs\activity_10981175453.tcx"

# Load the TCX file into a Python dictionary
with open(file, "r") as f:
    data = xmltodict.parse(f.read())

# Extract the activity data from the dictionary and convert it to a DataFrame
activity = data["TrainingCenterDatabase"]["Activities"]["Activity"]

df = pd.json_normalize(activity, record_path=["Lap", "Track", "Trackpoint"])

df["Time"] = pd.to_datetime(df["Time"])

df.columns.unique()

cols_to_convert = [
    "DistanceMeters",
    "HeartRateBpm.Value",
    "Extensions.ns3:TPX.ns3:Speed",
    "Extensions.ns3:TPX.ns3:RunCadence",
    "AltitudeMeters",
    "Position.LatitudeDegrees",
    "Position.LongitudeDegrees",
]


df[cols_to_convert] = df[cols_to_convert].astype(float)

df = df.dropna()


# Define the chart
chart = (
    alt.Chart(df)
    .mark_point()
    .encode(
        x=alt.X("DistanceMeters", scale=alt.Scale(zero=False)),
        y=alt.Y("AltitudeMeters", scale=alt.Scale(zero=False)),
    )
)
chart


# Define the chart
chart = (
    alt.Chart(df)
    .mark_point()
    .encode(
        x=alt.X("Time:T", axis=alt.Axis(format="%H:%M")),
        y=alt.Y("AltitudeMeters", scale=alt.Scale(zero=False)),
    )
)

chart

# Create a new figure
fig, ax = plt.subplots()


# Plot the data with timestamps on the x-axis
plt.scatter(df["Time"], df["HeartRateBpm.Value"])


formatter = da.dates.DateFormatter("%H:%M:%S")
ax.xaxis.set_major_formatter(formatter)

# Show the plot
plt.show()

# Elevation
# Pace ?
# Lap average pace
# Heart rate bpm
# Cadence - steps per minute (spm).
# Run/Walk

## stats

## Laps - shown as table


## Time in Zones - time and percentage shown

# Zone 5   > 169 bpm • Maximum
# Zone 4   150 - 168 bpm • Threshold
# Zone 3   132 - 149 bpm • Aerobic
# Zone 2   113 - 131 bpm • Easy
# Zone 1   94 - 112 bpm • Warm Up
