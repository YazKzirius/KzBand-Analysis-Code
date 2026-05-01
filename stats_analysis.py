#Important imports 
import numpy as np
from scipy.stats import wilcoxon


#This function performs wilcoxon test
def paired_wilcoxon(x, y):
    x = np.asarray(x)
    y = np.asarray(y)

    mask = ~np.isnan(x) & ~np.isnan(y)
    x = x[mask]
    y = y[mask]

    if len(x) < 3:
        return {
            "stat": np.nan,
            "p_value": np.nan,
            "effect_size": np.nan
        }

    try:
        stat, p = wilcoxon(x, y)
    except Exception:
        return {
            "stat": np.nan,
            "p_value": np.nan,
            "effect_size": np.nan
        }

    #effect size comparison 
    diff = x - y
    n_pos = np.sum(diff > 0)
    n_neg = np.sum(diff < 0)

    if (n_pos + n_neg) == 0:
        effect_size = 0
    else:
        effect_size = (n_pos - n_neg) / (n_pos + n_neg)

    return {
        "stat": stat,
        "p_value": p,
        "effect_size": effect_size
    }


#95% Confidence intervals
def bootstrap_ci(data, n_boot=1000, ci=95):
    data = np.asarray(data)
    data = data[~np.isnan(data)]

    if len(data) < 3:
        return (np.nan, np.nan)

    boot_means = []

    for _ in range(n_boot):
        sample = np.random.choice(data, size=len(data), replace=True)
        boot_means.append(np.mean(sample))

    lower = np.percentile(boot_means, (100 - ci) / 2)
    upper = np.percentile(boot_means, 100 - (100 - ci) / 2)

    return lower, upper
