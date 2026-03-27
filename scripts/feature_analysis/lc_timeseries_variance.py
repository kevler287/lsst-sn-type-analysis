from typing import List
from models.ztf_object import ZTFObject
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def count_days_for_filter(obj: ZTFObject, fid: int):
    unique_days = {
        "detections": set(),
        "non_detections": set(),
        "forced_photometry": set(),
    }
    for det in obj.detections:
        if det.fid == fid:
            unique_days["detections"].add(int(det.mjd))
    for nd in obj.non_detections:
        if nd.fid == fid:
            unique_days["non_detections"].add(int(nd.mjd))
    for fp in obj.forced_photometry:
        if fp.fid == fid:
            unique_days["forced_photometry"].add(int(fp.mjd))
    return unique_days

def analyze_lc_timeseries_length(ztf_objects: List[ZTFObject]):
    frame: pd.DataFrame = pd.DataFrame(columns=["fid", "n_det", "n_non_det", "n_fp"])
    for fid in [1,2,3]:
        for ztf_obj in ztf_objects:
            unique_days = count_days_for_filter(ztf_obj, fid)
            frame.loc[len(frame)] = [
                fid,
                len(unique_days["detections"]),
                len(unique_days["non_detections"]),
                len(unique_days["forced_photometry"]),
            ]
    result = frame.groupby("fid")[["n_det", "n_non_det", "n_fp"]].agg(["mean", "std"])
    print(result)
    return frame

def plot_lc_timeseries_length(ztf_objects: List[ZTFObject], fids=[1, 2, 3], filter_0: bool = True):
    frame = analyze_lc_timeseries_length(ztf_objects)

    fig, axes = plt.subplots(3, 1, figsize=(12, 15))
    fid_labels = {1: "g", 2: "r", 3: "i"}
    colors = ["#4CAF50", "#F44336", "#9C27B0"]
    width = 0.25
    columns = ["n_det", "n_non_det", "n_fp"]
    titles = ["detections", "non detections", "forced photometry"]

    all_x = sorted(set().union(*[frame[col].unique() for col in columns]))
    if filter_0:
        all_x = [x for x in all_x if x > 0]

    x = np.arange(len(all_x))
    for ax, col, title in zip(axes, columns, titles):

        for i, fid in enumerate(fids):
            counts = frame[frame["fid"] == fid][col].value_counts().reindex(all_x, fill_value=0)
            ax.bar(x + i * width, counts.values, width=width, label=f"fid {fid} ({fid_labels[fid]})", color=colors[i])

        step = 5
        ax.set_xticks(x[::step] + width)
        ax.set_xticklabels(all_x[::step])
        ax.set_xlabel("n days with observation")
        ax.set_ylabel("n ztf objects")
        ax.set_title(title)
        ax.legend()

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4)
    plt.show()