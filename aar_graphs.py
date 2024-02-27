import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import seaborn as sns
import pandas as pd
import scipy.stats as st
import random
import math
import warnings
import sys
import os

LINESTYLES = {
    "2sigma": "dotted",
    "mean_rolling": "solid",
    "mean_continuous": "dashdot",
    "threshold": "--",
    "win_count": "dotted"
}

def plot_component(df, title, component, ax, max_range, samples_per_step, window_size, stride, mirror_y_axis = True):
    # stride > window size = missing/inaccurate data in plots
    if stride > window_size:
        print("Error: stride must be smaller than window size.")
        return
    
    # if none specified, set range to capture all observations
    if max_range == None:
        max_range = max(df["distance"])
        
    # compute windowing params
    windows = np.arange(0, max_range + stride, stride)
    half_win = window_size / 2
    
    # temp storage of rolling means/standard devs/samples
    rolling_avg = []
    rolling_std = []
    rand_samples = {} # using a map instead of two arrays prevents duplicate entries
    
    # convert pandas dataframes to numpy arrays
    distances = df["distance"].to_numpy()
    errors = df[component].to_numpy()
    
    for w in windows:
        # get indices for observations within the current window
        indices = np.where((distances >= w-half_win) & (distances < w+half_win))
            
        # remove all nans from window
        win_err = list(filter(lambda x: not math.isnan(x), errors[indices]))
        
        if len(win_err) > 0:
            # compute rolling means/standard devs
            rolling_avg.append(np.mean(win_err))
            rolling_std.append(np.std(win_err))
        else:
            rolling_avg.append(np.nan)
            rolling_std.append(np.nan)
            
        # randomly sample error values
        batch = min(len(indices[0]), samples_per_step)
        rand_sample = random.sample(sorted(indices[0]), batch)
        for idx in rand_sample:
            rand_samples[idx] = (distances[idx], errors[idx])
            
    rand_samples = list(rand_samples.items())
    samples_dist = []
    samples_errs = []
    
    for key, val in rand_samples:
        samples_dist.append(val[0])
        samples_errs.append(val[1])
    
    # convert rolling values to pandas dataframes
    plot_df = pd.DataFrame(np.transpose([rolling_avg, rolling_std]), columns=['mean', 'std'])
    # ...so we can use it to do some math
    plus_2_sigma = plot_df["mean"] + 2 * plot_df["std"]
    minus_2_sigma = plot_df["mean"] - 2 * plot_df["std"]

    xlim = [0,max_range]
    ylim = [0, .4]
    
    if mirror_y_axis:
        ylim[0] = -.4

    # Set the axes to the new limits
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    # top threshold
    ax.hlines(y=0.07, xmin=xlim[0], xmax=xlim[1], linewidth=1, linestyle=LINESTYLES["threshold"], color="gray", zorder=1)
    if mirror_y_axis:
        # bottom threshold
        ax.hlines(y=-0.07, xmin=xlim[0], xmax=xlim[1], linewidth=1, linestyle=LINESTYLES["threshold"],  color="gray", zorder=1)
        # centerline (zero)
        ax.hlines(y=0, xmin=xlim[0], xmax=xlim[1], linewidth=1, color="black", zorder=1)
    # 2 standard deviations from the mean
    ax.fill_between(windows, plus_2_sigma, minus_2_sigma, color="tab:blue", alpha=0.2, zorder=2)
    # random samples (per window step)
    ax.scatter(samples_dist, samples_errs, marker=".", s=4, zorder=3)
    # rolling mean
    ax.plot(windows, rolling_avg, label="Mean Rolling", linewidth=1, linestyle=LINESTYLES["mean_rolling"], color="red", zorder=4)
    ax.invert_xaxis()
    ax.set_ylabel("Error (m)")
    ax.set_title(title)

def plot_reliability(df, title, ax, max_range, samples_per_step, window_size, stride):
    # stride > window size = missing/inaccurate data in plots
    if stride > window_size:
        print("Error: stride must be smaller than window size.")
        return
    
    # if none specified, set range to capture all observations
    if max_range == None:
        max_range = max(df["distance"])
        
    # compute windowing params
    windows = np.arange(0, max_range + stride, stride)
    half_win = window_size / 2
    
    # temp storage of reliability and window count
    reliability = []
    win_cnt = []
    
    # convert pandas dataframes to numpy arrays
    distances = df["distance"].to_numpy()
    errors = df["mag"].to_numpy()
    
    for w in windows:
        # get indices for observations within the current window
        indices = np.where((distances >= w-half_win) & (distances < w+half_win))
        
        # compute reliability of window
        count_all = len(errors[indices])
        win_cnt.append(count_all)
        count_nan = np.count_nonzero(np.isnan(errors[indices]))
        if count_all > 0:
            reliability.append((count_all-count_nan)/count_all)
        else:
            reliability.append(np.nan)
    
    xlim = [0,max_range]
    ylim = [0, 1.0]

    # Set the axes to the new limits
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    # reliability percentages
    ax.fill_between(windows, 0, reliability, color="tab:green", alpha=0.2, zorder=1)
    ax.invert_xaxis()
    ax.set_xlabel("True Distance Between Probe and Drogue (m)")
    ax.set_ylabel("Success (%)")
    ax.set_title(title)
    
    # count
    ax2 = ax.twinx()
    ax2.plot(windows, win_cnt, label="Sample Count", linewidth=1, linestyle=LINESTYLES["win_count"], color="black", zorder=2)
    ax2.set_ylabel("Count")
    
max_range = None

if len(sys.argv) != 6 and len(sys.argv) != 7:
    script_file_name = os.path.basename(__file__)
    print(f"Usage: python3 {script_file_name} <csvfile> <output> <win_size> <stride> <samples_per_step> [<max_range>]")
    sys.exit(1)
elif len(sys.argv) == 7:
    max_range = float(sys.argv[6])

csvfile = sys.argv[1]
output = sys.argv[2]
win_size = float(sys.argv[3])
stride = float(sys.argv[4])
samples_per_step = int(sys.argv[5])

components = ["mag", "dx", "dy", "dz"]
titles = ["Magnitude", "X Component", "Y Component", "Z Component", "Reliability"]
# load true distance with x, y, and z error
print("Loading data from file.")
df = pd.read_csv(csvfile)
print("Generating error plots.")
# compute truth distance
df["distance"] = df.apply(lambda row: np.sqrt(row["tru_x"] ** 2 + row["tru_y"] ** 2 + row["tru_z"] ** 2), axis=1)
# compute the error components
df["dx"] = df.apply(lambda row: row["tru_x"] - row["est_x"] , axis=1)
df["dy"] = df.apply(lambda row: row["tru_y"] - row["est_y"] , axis=1)
df["dz"] = df.apply(lambda row: row["tru_z"] - row["est_z"] , axis=1)
# compute magnitude error
df["mag"] = df.apply(lambda row: np.sqrt(row["dx"] ** 2 + row["dy"] ** 2 + row["dz"] ** 2), axis=1)

height_ratios = [1, 1, 1, 1, 0.6]
fig, axs = plt.subplots(nrows=5, ncols=1, figsize=(8.5, 10.15), constrained_layout=True, gridspec_kw={'height_ratios': height_ratios})

plot_component(  df, titles[0], components[0], axs[0], max_range, samples_per_step, win_size, stride, False)
plot_component(  df, titles[1], components[1], axs[1], max_range, samples_per_step, win_size, stride)
plot_component(  df, titles[2], components[2], axs[2], max_range, samples_per_step, win_size, stride)
plot_component(  df, titles[3], components[3], axs[3], max_range, samples_per_step, win_size, stride)
plot_reliability(df, titles[4],                axs[4], max_range, samples_per_step, win_size, stride)

custom_lines = [
    Line2D([0], [0], color="red", lw=2, linestyle=LINESTYLES["mean_rolling"]),
    Patch(facecolor="tab:blue", alpha=0.2),
    Line2D([0], [0], marker="o", color="White", lw=2, markerfacecolor="tab:blue"),
    Line2D([0], [0], color="black", lw=1.6, linestyle=LINESTYLES["win_count"]),
    Line2D([0], [0], color="gray", lw=1.4, linestyle=LINESTYLES["threshold"])
]

custom_descriptors = [
    "Mean (Rolling)",
    "\u00B12\u03c3 (Rolling)",
    "Random Sample",
    "Observation Count",
    "Acceptable Threshold (\u00B17cm)"
]

if samples_per_step==0:
    del custom_lines[2]
    del custom_descriptors[2]
    legend_loc = (0.76, 1.06)
else:
    legend_loc = (0.76, 1.08)

fig.legend(custom_lines, custom_descriptors, loc="upper right", ncol=2, fancybox=True, shadow=True, bbox_to_anchor=legend_loc)

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=UserWarning)
    plt.tight_layout(rect=[0, 0, 1, 1])

print(f"Saving plots to: {output}", end=None)
plt.savefig(output, bbox_inches='tight')
print("Done")