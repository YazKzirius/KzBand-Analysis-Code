#Important imports
import os
import sys
import traceback
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
from config import PHASES, TIME_ALIGNMENT_TOLERANCE
from load_data import load_kzband, load_kzhand, load_polar
from preprocess import align_time
from features import (
    eda_metrics,
    hr_metrics,
    temperature_metrics,
    kinematic_metrics
)
from bland_altman import bland_altman
from relationships import stress_performance
from plotting import plot_bland_altman, plot_multisignal_timeseries
from scipy.stats import binomtest
from stats_analysis import paired_wilcoxon, bootstrap_ci


#Specific output paths
DATA_ROOT = "data"
OUT_ROOT = "outputs"
os.makedirs(f"{OUT_ROOT}/tables", exist_ok=True)
os.makedirs(f"{OUT_ROOT}/figures/timeseries", exist_ok=True)
os.makedirs(f"{OUT_ROOT}/figures/bland_altman", exist_ok=True)
all_results = []


#This file finds specific datasets
def find_file(folder, keyword):
    for f in os.listdir(folder):
        if keyword.lower() in f.lower():
            return os.path.join(folder, f)
    return None

for group in ["pilot", "participants"]:
    group_path = os.path.join(DATA_ROOT, group)
    if not os.path.exists(group_path):
        continue
    for pid in os.listdir(group_path):
        pid_path = os.path.join(group_path, pid)
        if not os.path.isdir(pid_path):
            continue

        for phase in os.listdir(pid_path):
            phase_path = os.path.join(pid_path, phase)
            if not os.path.isdir(phase_path):
                continue

            metrics = {
                "participant": pid,
                "group": group,
                "phase": phase,
                "analysis_error": ""
            }

            try:
                #Finding Specific device files
                kzband_path = find_file(phase_path, "kzband")
                kzhand_path = find_file(phase_path, "kzhand")
                polar_path  = find_file(phase_path, "polar")

                band = hand = polar = None

                #Headband processing
                if kzband_path:
                    band = load_kzband(kzband_path)
                    metrics.update(eda_metrics(band))
                    metrics.update(temperature_metrics(band))
                    metrics.update(kinematic_metrics(band))

                    if "bpm" in band.columns:
                        metrics.update(hr_metrics(band))

               #Reference device processing
                if kzhand_path:
                    hand = load_kzhand(kzhand_path)

                if polar_path:
                    polar = load_polar(polar_path)

                #Combined timeseries graphs for individual signals
                signals = []

                if polar is not None and "polar_hr" in polar.columns:
                    signals.append({
                        "df": polar,
                        "time_col": "time_s",
                        "value_col": "polar_hr",
                        "ylabel": "Heart Rate (BPM)",
                        "label": "Polar HR"
                    })

                if band is not None and "bpm" in band.columns:
                    signals.append({
                        "df": band,
                        "time_col": "time_s",
                        "value_col": "bpm",
                        "ylabel": "Heart Rate (BPM)",
                        "label": "Forehead HR"
                    })

                if band is not None and "eda_forehead_phasic" in band.columns:
                    signals.append({
                        "df": band,
                        "time_col": "time_s",
                        "value_col": "eda_forehead_phasic",
                        "ylabel": "Forehead EDA (µS)",
                        "label": "Forehead EDA"
                    })

                if hand is not None and "eda_finger_phasic" in hand.columns:
                    signals.append({
                        "df": hand,
                        "time_col": "time_s",
                        "value_col": "eda_finger_phasic",
                        "ylabel": "Finger EDA (µS)",
                        "label": "Finger EDA"
                    })

                if band is not None and "acc_mag" in band.columns:
                    signals.append({
                        "df": band,
                        "time_col": "time_s",
                        "value_col": "acc_mag",
                        "ylabel": "Acceleration Magnitude (g)",
                        "label": "Acceleration"
                    })

                if band is not None and "gyro_mag" in band.columns:
                    signals.append({
                        "df": band,
                        "time_col": "time_s",
                        "value_col": "gyro_mag",
                        "ylabel": "Angular Velocity (°/s)",
                        "label": "Angular Velocity"
                    })

                if signals:
                    plot_multisignal_timeseries(
                        signals,
                        title=f"{pid} {phase} Physiological & Kinematic Time-Series",
                        path=f"{OUT_ROOT}/figures/timeseries/{pid}_{phase}_Combined.png"
                    )

                #Bland altman analysis for heart-rate
                if band is not None and polar is not None and "bpm" in band.columns:
                    merged_hr = align_time(
                        band[["time_s", "bpm"]],
                        polar,
                        TIME_ALIGNMENT_TOLERANCE
                    )
                    if not merged_hr.empty:
                        ba_hr = bland_altman(
                            merged_hr["bpm"],
                            merged_hr["polar_hr"]
                        )
                        plot_bland_altman(
                            ba_hr,
                            f"{pid} {phase} HR Bland–Altman",
                            f"{OUT_ROOT}/figures/bland_altman/{pid}_{phase}_HR.png",
                            "Forehead HR − Polar HR (BPM)"
                        )

                #Bland altman analysis for EDA
                if band is not None and hand is not None:
                    if (
                        "eda_forehead_phasic" in band.columns and
                        "eda_finger_phasic" in hand.columns
                    ):
                        merged_eda = align_time(
                            band[["time_s", "eda_forehead_phasic"]],
                            hand[["time_s", "eda_finger_phasic"]],
                            TIME_ALIGNMENT_TOLERANCE
                        )
                        if not merged_eda.empty:
                            ba_eda = bland_altman(
                                merged_eda["eda_finger_phasic"],
                                merged_eda["eda_forehead_phasic"]
                            )
                            plot_bland_altman(
                                ba_eda,
                                f"{pid} {phase} EDA Bland–Altman",
                                f"{OUT_ROOT}/figures/bland_altman/{pid}_{phase}_EDA.png",
                                "Finger EDA − Forehead EDA (µS)"
                            )
                            
                #Stress-performance relationships
                if band is not None and phase in PHASES:
                    metrics.update(stress_performance(band))

            except Exception as e:
                err = f"{e}"
                traceback.print_exc()
                metrics["analysis_error"] = err
            out_csv = f"{OUT_ROOT}/tables/{pid}_{phase}_metrics.csv"
            pd.DataFrame([metrics]).to_csv(out_csv, index=False)
            all_results.append(metrics)

#Final Summary Table
if all_results:
    summary_df = pd.DataFrame(all_results)
    summary_df = summary_df.sort_values(
        by=["group", "participant", "phase"]
    )
    summary_path = f"{OUT_ROOT}/tables/Table_Final_Summary_All_Participants.csv"
    summary_df.to_csv(summary_path, index=False)


#Statistical analysis 
df_stats = summary_df[summary_df["group"] == "participants"]

phase_results = []
sign_results = []

if not df_stats.empty:
    #Phase comparison test
    pivot = df_stats.pivot_table(
        index="participant",
        columns="phase",
        values=["mean_phasic_eda", "mean_hr", "mean_acc", "mean_gyro"],
        aggfunc="mean"
    )

    for metric in ["mean_phasic_eda", "mean_hr", "mean_acc", "mean_gyro"]:
        try:
            if ("Predictable" in pivot[metric].columns and
                "Unpredictable" in pivot[metric].columns):

                pred = pivot[(metric, "Predictable")].values
                unpred = pivot[(metric, "Unpredictable")].values

                res = paired_wilcoxon(unpred, pred)

                diff = unpred - pred
                ci_low, ci_high = bootstrap_ci(diff)

                print(f"\n{metric}:")
                print(f"  p-value: {res['p_value']:.4f}")
                print(f"  effect size: {res['effect_size']:.3f}")
                print(f"  CI: [{ci_low:.3f}, {ci_high:.3f}]")
                phase_results.append({
                    "metric": metric,
                    "p_value": res["p_value"],
                    "effect_size": res["effect_size"],
                    "ci_lower": ci_low,
                    "ci_upper": ci_high
                })

        except Exception as e:
            print(f"{e}")

    #Sign test comparison
    for metric in [
        "eda_acc_spearman",
        "eda_gyro_spearman",
        "hr_acc_spearman",
        "hr_gyro_spearman"
    ]:
        try:
            vals = df_stats[metric].dropna()

            if len(vals) < 3:
                continue

            n_pos = (vals > 0).sum()
            n_total = len(vals)

            test = binomtest(n_pos, n_total, p=0.5)

            print(f"\n{metric}:")
            print(f"  Positive: {n_pos}/{n_total}")
            print(f"  p-value: {test.pvalue:.4f}")

            sign_results.append({
                "metric": metric,
                "n_positive": n_pos,
                "n_total": n_total,
                "p_value": test.pvalue
            })

        except Exception as e:
            print(f"{e}")

    #Save tables in specific folders
    phase_df = pd.DataFrame(phase_results)
    sign_df = pd.DataFrame(sign_results)

    phase_path = f"{OUT_ROOT}/tables/Stats_Phase_Comparison.csv"
    sign_path = f"{OUT_ROOT}/tables/Stats_Sign_Test.csv"

    phase_df.to_csv(phase_path, index=False)
    sign_df.to_csv(sign_path, index=False)

else:
    print("No participant data available")
