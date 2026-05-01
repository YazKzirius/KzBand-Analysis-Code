#Important imports
import numpy as np

#This function perfoms blant-altman analysis between two variables
def bland_altman(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    mask = ~np.isnan(x) & ~np.isnan(y)
    x = x[mask]
    y = y[mask]

    diff = x - y
    mean = (x + y) / 2

    bias = diff.mean()
    sd = diff.std(ddof=1)

    return {
        "mean": mean,
        "diff": diff,
        "bias": bias,
        "sd": sd,
        "loa_upper": bias + 1.96 * sd,
        "loa_lower": bias - 1.96 * sd
    }
