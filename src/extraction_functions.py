import xml.etree.ElementTree as ET
import xmltodict
import pandas as pd
import os
import glob


def extract_gpx_data(file_path):
    """
    This function parses a GPX (GPS Exchange Format) file and extracts specific data, including latitude, longitude, elevation, time, heart rate, and cadence, from the trackpoints. The extracted data is returned as a pandas DataFrame.

    Args:
        file_path (string): The path to the GPX file to be parsed.

    Returns:
        df (pandas DataFrame): A DataFrame containing the extracted data from the GPX file.
    """
    # Parse the GPX file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Define namespaces
    namespaces = {
        "gpx": "http://www.topografix.com/GPX/1/1",
        "ns3": "http://www.garmin.com/xmlschemas/TrackPointExtension/v1",
    }

    # Extract the desired data
    data = []
    for trkpt in root.findall(".//gpx:trkpt", namespaces):
        lat = trkpt.get("lat")
        lon = trkpt.get("lon")
        ele = trkpt.find("gpx:ele", namespaces).text
        time = trkpt.find("gpx:time", namespaces).text
        hr = trkpt.find(".//ns3:hr", namespaces).text
        cad = trkpt.find(".//ns3:cad", namespaces).text

        data.append(
            {"lat": lat, "lon": lon, "ele": ele, "time": time, "hr": hr, "cad": cad}
        )

    cols_to_convert = [
        "lat",
        "lon",
        "ele",
        "hr",
        "cad",
    ]

    # Create a pandas DataFrame
    df = pd.DataFrame(data)

    # Convert to float
    df[cols_to_convert] = df[cols_to_convert].astype(float)

    # Convert to datetime
    df["time"] = pd.to_datetime(df["time"])

    return df


def extract_tcx_data(directory):
    """
    This function extracts data from TCX (Training Center XML) files located in a specified directory. It loads each TCX file into a Python dictionary, extracts the activity data, and converts it into a pandas DataFrame. The function returns a merged DataFrame containing data from all the TCX files.

    Args:
        directory (string): The directory path containing the TCX files.

    Returns:
        merged_df (pandas DataFrame): A DataFrame that combines the extracted data from all TCX files.
    """
    # Get a list of all TCX files in the directory
    tcx_files = glob.glob(os.path.join(directory, "*.tcx"))

    # List to store individual DataFrames
    dfs = []

    for file_path in tcx_files:
        # Load the TCX file into a Python dictionary
        with open(file_path, "r") as f:
            data = xmltodict.parse(f.read())

        # Extract the activity data from the dictionary
        activity = data["TrainingCenterDatabase"]["Activities"]["Activity"]

        # Conversion to DataFrame
        df = pd.json_normalize(activity, record_path=["Lap", "Track", "Trackpoint"])

        cols_to_convert = [
            "AltitudeMeters",
            "DistanceMeters",
            "Position.LatitudeDegrees",
            "Position.LongitudeDegrees",
            "HeartRateBpm.Value",
            "Extensions.ns3:TPX.ns3:Speed",
            "Extensions.ns3:TPX.ns3:RunCadence",
        ]

        df = df.dropna(axis=0)

        # Convert to float
        df[cols_to_convert] = df[cols_to_convert].astype(float)

        # Convert to datetime
        df["Time"] = pd.to_datetime(df["Time"])

        dfs.append(df)

    # Merge all DataFrames into a single DataFrame
    merged_df = pd.concat(dfs, ignore_index=True)

    return merged_df


def extract_general_tcx_data(directory):
    """
    This function extracts general data from TCX (Training Center XML) files located in a specified directory. It loads each TCX file into a Python dictionary, extracts the activity data, performs data conversions and transformations, and merges the extracted data into a single pandas DataFrame. The function returns the merged DataFrame containing the general TCX data.

    Args:
        directory (string): The directory path containing the TCX files.

    Returns:
        merged_df (pandas DataFrame): A DataFrame that combines the extracted general data from all TCX files.
    """
    # Get a list of all TCX files in the directory
    tcx_files = glob.glob(os.path.join(directory, "*.tcx"))

    # List to store individual DataFrames
    dfs = []

    for file_path in tcx_files:
        # Load the TCX file into a Python dictionary
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

        # Convert to datetime
        df["@StartTime"] = pd.to_datetime(df["@StartTime"])

        df = df.dropna(axis=0)

        # Convert to float
        df[cols_to_float] = df[cols_to_float].astype(float)

        # Convert to int
        df[cols_to_int] = df[cols_to_int].astype(int)

        dfs.append(df)

    # Merge all DataFrames into a single DataFrame
    merged_df = pd.concat(dfs, ignore_index=True)

    return merged_df
