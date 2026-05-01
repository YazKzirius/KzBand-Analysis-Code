#Important imports
from scipy.stats import spearmanr
import numpy as np
import warnings

#The function calculates spearman stats for metrics
def safe_spearman(x, y):
    if len(x) < 3:
        return np.nan
    if np.nanstd(x) == 0 or np.nanstd(y) == 0:
        return np.nan
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return spearmanr(x, y).correlation

#This function quantifies the relationship between stress and kinematic performance
def stress_performance(df):
    results = {}
    if "eda_forehead_phasic" in df.columns and "acc_mag" in df.columns:
        mask = ~df["eda_forehead_phasic"].isna() & ~df["acc_mag"].isna()
        results["eda_acc_spearman"] = safe_spearman(
            df.loc[mask, "eda_forehead_phasic"],
            df.loc[mask, "acc_mag"]
        )
    if "eda_forehead_phasic" in df.columns and "gyro_mag" in df.columns:
        mask = ~df["eda_forehead_phasic"].isna() & ~df["gyro_mag"].isna()
        results["eda_gyro_spearman"] = safe_spearman(
            df.loc[mask, "eda_forehead_phasic"],
            df.loc[mask, "gyro_mag"]
        )
    if "bpm" in df.columns and "acc_mag" in df.columns:
        mask = ~df["bpm"].isna() & ~df["acc_mag"].isna()
        results["hr_acc_spearman"] = safe_spearman(
            df.loc[mask, "bpm"],
            df.loc[mask, "acc_mag"]
        )
    if "bpm" in df.columns and "gyro_mag" in df.columns:
        mask = ~df["bpm"].isna() & ~df["gyro_mag"].isna()
        results["hr_gyro_spearman"] = safe_spearman(
            df.loc[mask, "bpm"],
            df.loc[mask, "gyro_mag"]
        )
    return results
