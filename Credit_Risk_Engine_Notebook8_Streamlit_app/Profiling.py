import pandas as pd
from ydata_profiling import ProfileReport


df = pd.read_csv("merge_data_imputed.csv")
profile = ProfileReport(df, title="Data Profile")
profile.to_file("/data/data_profile.html")