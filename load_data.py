#Important imports
import pandas as pd

#This function loads kzband csv files for participants
def load_kzband(path):
    data_frame = pd.read_csv(path)
    data_frame["time_s"] = data_frame["timestamp_ms"] / 1000
    return data_frame

#This function loads kzhand csv files for participants
def load_kzhand(path):
    data_frame = pd.read_csv(path)
    data_frame["time_s"] = data_frame["timestamp_ms"] / 1000
    return data_frame

#This function loads Polar H10 csv files for participants
def load_polar(path):
    data_frame = pd.read_csv(path, skiprows = 2)
    data_frame = data_frame[["Time", "HR (bpm)"]].dropna()
    data_frame["time_s"] = pd.to_timedelta(data_frame["Time"]).dt.total_seconds()
    data_frame.rename(columns={"HR (bpm)": "polar_hr"}, inplace=True)
    return data_frame
