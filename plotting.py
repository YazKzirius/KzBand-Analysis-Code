#Important imports
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import re


#This function gets specific units for metric
def _extract_unit(label):
    match = re.search(r"\((.*?)\)", label)
    return match.group(1) if match else ""



#This function plots bland altman
def plot_bland_altman(stats, title, path, ylabel):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    unit = _extract_unit(ylabel)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(stats["mean"], stats["diff"], alpha=0.6)
    ax.axhline(stats["bias"], color="red", label="Bias")
    ax.axhline(stats["loa_upper"], linestyle="--", color="green", label="+1.96 SD")
    ax.axhline(stats["loa_lower"], linestyle="--", color="green", label="−1.96 SD")
    ax.set_xlabel(f"Mean ({unit})" if unit else "Mean")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)

#This function plots multiple time series for sensor in a subplot
def plot_multisignal_timeseries(signals, title, path, xlabel="Time (s)"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    n = len(signals)
    fig, axes = plt.subplots(n, 1, figsize=(8, 2.3 * n), sharex=True)
    if n == 1:
        axes = [axes]
    for ax, sig in zip(axes, signals):
        df = sig["df"]
        ax.plot(
            df[sig["time_col"]],
            df[sig["value_col"]],
            linewidth=1
        )
        ax.set_ylabel(sig["ylabel"])
        ax.set_title(sig.get("label", ""))
        ax.grid(alpha=0.3)
    axes[-1].set_xlabel(xlabel)
    fig.suptitle(title)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
