import pandas as pd
import extraction_functions as ef


# Specify the GPX file path
# gpx_file = r"./data/activity_11182302898.gpx"
# tcx_file = r"./data/activity_11182302898.tcx"


tcx_file = r"C:\Users\paulh\Desktop\Fitness\data"


# Extract data from GPX file and save to DataFrame
# df_gpx = ef.extract_gpx_data(gpx_file)
df_tcx = ef.extract_tcx_data(tcx_file)
df_general_tcx = ef.extract_general_tcx_data(tcx_file)

# df_general_tcx.columns.unique()
df_tcx.dtypes
df_general_tcx.dtypes

# save dataframe
# df_gpx.to_pickle(r"./data/gpx-data.pkl")
df_tcx.to_pickle(r"./data/merged-tcx-data.pkl")
df_general_tcx.to_pickle(r"./data/merged-general-tcx-data.pkl")
