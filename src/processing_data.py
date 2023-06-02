import extraction_functions as ef


# Specify the GPX file path
tcx_file = r"./data/activity_11182302898.tcx"
# tcx_file = r"C:\Users\paulh\Desktop\Fitness\data"

# Extract data from GPX file and save to DataFrame
df_tcx = ef.extract_tcx_data(tcx_file)
df_general_tcx = ef.extract_general_tcx_data(tcx_file)

# save dataframe
df_tcx.to_pickle(r"./data/merged-tcx-data.pkl")
df_general_tcx.to_pickle(r"./data/merged-general-tcx-data.pkl")
