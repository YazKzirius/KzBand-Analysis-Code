#Important imports
import pandas as pd

#The function aligning timestamps based on 1.0 second tolerance
def align_time (df1, df2, tolerance):
    return pd.merge_asof(df1.sort_values("time_s"),
                         df2.sort_values("time_s"),
                         on="time_s",
                         direction = "nearest",
                         tolerance = tolerance).dropna()


