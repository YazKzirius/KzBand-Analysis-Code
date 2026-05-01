#Important imports
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

#Specific directory names
TABLE_DIR = "outputs/tables"
FIG_DIR = "outputs/figures/results"
TABLE_OUT = os.path.join(FIG_DIR, "tables")

os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(TABLE_OUT, exist_ok=True)

#loading data frames 
dfs = []
for f in os.listdir(TABLE_DIR):
    if f.endswith("_metrics.csv"):
        dfs.append(pd.read_csv(os.path.join(TABLE_DIR, f)))

df = pd.concat(dfs, ignore_index=True)


#Ordering data to specific phases
phase_order = ["Baseline", "Stretching", "Predictable", "Unpredictable", "Recovery"]
df["phase"] = pd.Categorical(
    df["phase"],
    categories=phase_order,
    ordered=True
)

#Plotting Forehead heart rate across phases
plt.figure(figsize=(7, 4))
for pid in df["participant"].unique():
    sub = df[df["participant"] == pid]
    plt.plot(sub["phase"].cat.codes, sub["mean_hr"], alpha=0.5)

plt.xticks(range(len(phase_order)), phase_order, rotation=30)
plt.ylabel("Heart Rate (BPM)")
plt.xlabel("Experimental Phase")
plt.title("Group-Level Forehead Heart Rate Across Phases")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "Fig6_4_Group_Forehead_HR.png"), dpi=300)
plt.close()

#Plotting Forehead Phasic EDA across phases
plt.figure(figsize=(7, 4))
for pid in df["participant"].unique():
    sub = df[df["participant"] == pid]
    plt.plot(sub["phase"].cat.codes, sub["mean_phasic_eda"], alpha=0.5)

plt.xticks(range(len(phase_order)), phase_order, rotation=30)
plt.ylabel("Phasic EDA (µS)")
plt.xlabel("Experimental Phase")
plt.title("Group-Level Forehead Phasic EDA Across Phases")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "Fig6_5_Group_Forehead_EDA.png"), dpi=300)
plt.close()

#Creating EDA metrics table in CSV file
eda_table = (
    df.groupby("phase", observed=False)
      .agg(
          mean_phasic_eda_uS=("mean_phasic_eda", "mean"),
          sd_phasic_eda_uS=("mean_phasic_eda", "std"),
          scr_rate_per_min=("scr_rate", "mean"),
          mean_tonic_eda_uS=("mean_tonic_eda", "mean"),
          sd_tonic_eda_uS=("mean_tonic_eda", "std"),
      )
      .reset_index()
)

eda_table.to_csv(
    os.path.join(TABLE_OUT, "Table6_1_Forehead_EDA_By_Phase.csv"),
    index=False
)

plt.figure(figsize=(6, 4))
df.boxplot(column="mean_phasic_eda", by="phase")
plt.title("Distribution of Forehead Phasic EDA by Phase")
plt.suptitle("")
plt.ylabel("Phasic EDA (µS)")
plt.xlabel("Experimental Phase")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "Fig6_6_Phased_EDA_Boxplot.png"), dpi=300)
plt.close()

#Plotting Distribution box plots for heart-rate over phases
plt.figure(figsize=(6, 4))
df.boxplot(column="mean_hr", by="phase")
plt.title("Distribution of Forehead Heart Rate by Phase")
plt.suptitle("")
plt.ylabel("Heart Rate (BPM)")
plt.xlabel("Experimental Phase")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "Fig6_6b_Phased_HR_Boxplot.png"), dpi=300)
plt.close()

#Plotting bar bar plots for temperature over phases
plt.figure(figsize=(6, 4))
(
    df.groupby("phase", observed=False)["mean_temp"]
      .mean()
      .plot(kind="bar", yerr=df.groupby("phase", observed=False)["mean_temp"].std())
)

plt.ylabel("Temperature (°C)")
plt.xlabel("Experimental Phase")
plt.title("Forehead Temperature Across Experimental Phases")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "Fig6_7_Temperature_By_Phase.png"), dpi=300)
plt.close()


#Plotting Tempature Time Seiries over experimental phases 
plt.figure(figsize=(7, 4))
for pid in df["participant"].unique():
    sub = df[df["participant"] == pid]
    plt.plot(sub["phase"].cat.codes, sub["mean_temp"], alpha=0.5)

plt.xticks(range(len(phase_order)), phase_order, rotation=30)
plt.ylabel("Temperature (°C)")
plt.xlabel("Experimental Phase")
plt.title("Group-Level Forehead Temperature Across Phases")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "Fig6_7b_Group_Temperature.png"), dpi=300)
plt.close()

#Plotting kinematic via acceleration and angular velocity over phases 
plt.figure(figsize=(6, 4))
df.boxplot(column="mean_acc", by="phase")
plt.title("Acceleration Magnitude by Phase")
plt.suptitle("")
plt.ylabel("Acceleration Magnitude (g)")
plt.xlabel("Experimental Phase")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "Fig6_8_AccMag_By_Phase_Boxplot.png"), dpi=300)
plt.close()

plt.figure(figsize=(6, 4))
df.boxplot(column="mean_gyro", by="phase")
plt.title("Angular Velocity by Phase")
plt.suptitle("")
plt.ylabel("Angular Velocity (°/s)")
plt.xlabel("Experimental Phase")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "Fig6_9_GyroMag_By_Phase_Boxplot.png"), dpi=300)
plt.close()

#Kinematic time series over phases 
plt.figure(figsize=(7, 4))
for pid in df["participant"].unique():
    sub = df[df["participant"] == pid]
    plt.plot(sub["phase"].cat.codes, sub["mean_acc"], alpha=0.5)

plt.xticks(range(len(phase_order)), phase_order, rotation=30)
plt.ylabel("Acceleration Magnitude (g)")
plt.xlabel("Experimental Phase")
plt.title("Group-Level Acceleration Magnitude Across Phases")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "Fig6_10_Group_AccMag.png"), dpi=300)
plt.close()

plt.figure(figsize=(7, 4))
for pid in df["participant"].unique():
    sub = df[df["participant"] == pid]
    plt.plot(sub["phase"].cat.codes, sub["mean_gyro"], alpha=0.5)

plt.xticks(range(len(phase_order)), phase_order, rotation=30)
plt.ylabel("Angular Velocity (°/s)")
plt.xlabel("Experimental Phase")
plt.title("Group-Level Angular Velocity Across Phases")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "Fig6_11_Group_GyroMag.png"), dpi=300)
plt.close()

#Scatter plots for stress kinematic relationship
plt.figure(figsize=(6, 5))
plt.scatter(df["mean_phasic_eda"], df["mean_acc"], alpha=0.6)
plt.xlabel("Phasic EDA (µS)")
plt.ylabel("Acceleration Magnitude (g)")
plt.title("Forehead Phasic EDA vs Acceleration Magnitude")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "Fig6_12_EDA_vs_AccMag.png"), dpi=300)
plt.close()

plt.figure(figsize=(6, 5))
plt.scatter(df["mean_hr"], df["mean_acc"], alpha=0.6)
plt.xlabel("Heart Rate (BPM)")
plt.ylabel("Acceleration Magnitude (g)")
plt.title("Forehead Heart Rate vs Acceleration Magnitude")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "Fig6_13_HR_vs_AccMag.png"), dpi=300)
plt.close()

plt.figure(figsize=(6, 5))
plt.scatter(df["mean_phasic_eda"], df["mean_gyro"], alpha=0.6)
plt.xlabel("Phasic EDA (µS)")
plt.ylabel("Angular Velocity (°/s)")
plt.title("Forehead Phasic EDA vs Angular Velocity")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "Fig6_14_EDA_vs_GyroMag.png"), dpi=300)
plt.close()

plt.figure(figsize=(6, 5))
plt.scatter(df["mean_hr"], df["mean_gyro"], alpha=0.6)
plt.xlabel("Heart Rate (BPM)")
plt.ylabel("Angular Velocity (°/s)")
plt.title("Forehead Heart Rate vs Angular Velocity")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "Fig6_15_HR_vs_GyroMag.png"), dpi=300)
plt.close()

