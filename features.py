#Important imports
import numpy as np

#This function analyses specific eda metrics 
def eda_metrics(df):
    phasic = df ["eda_forehead_phasic"]
    tonic = df["eda_forehead_clean"] - phasic
    return {
        "mean_phasic_eda": np.nanmean(phasic),
        "std_phasic_eda": np.nanstd(phasic),
        "scr_rate": np.sum(phasic > 0.05) / len(phasic),
        "mean_tonic_eda": np.nanmean(tonic),
        "std_tonic_eda": np.nanstd(tonic)
                                  }

#This function analyses specific hr metrics 
def hr_metrics(df):
    return {
        "mean_hr": df["bpm"].mean(),
        "std_hr": df["bpm"].std(),
        "max_hr": df["bpm"].max()
        }

#This function analyses specific temperature metrics 
def temperature_metrics(df):
    return {
        "mean_temp": df["temperature_c"].mean(),
        "max_temp": df["temperature_c"].max(),
        "temp_change": df["temperature_c"].iloc[-1] - df["temperature_c"].iloc[0]
    }


#This function analyses specific kinematic metrics 
def kinematic_metrics(df):
    return {
        "mean_acc": df["acc_mag"].mean(),
        "peak_acc": df["acc_mag"].max(),
        "mean_gyro": df["gyro_mag"].mean(),
        "peak_gyro": df["gyro_mag"].max(),
         "high_motion_ratio": (df["motion_state"] == "HIGH").mean()
        }
        
