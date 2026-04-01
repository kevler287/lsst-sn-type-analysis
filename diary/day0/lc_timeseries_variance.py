import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import List, Tuple
from models.ztf_object import ZTFObject
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from api.mongo_client import LSSTMongoClient
from models.tns_object import TNSObject

fid_labels = {1: "g", 2: "r", 3: "i"}
colors = ["#4CAF50", "#F44336", "#9C27B0"]
width = 0.25
titles = ["detections", "non detections", "forced photometry"]

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

def analyze_lc_timeseries(ztf_objects: List[ZTFObject]):
    frame: pd.DataFrame = pd.DataFrame(columns=["fid", "n_det", "d_det", "n_non_det", "d_non_det", "n_fp", "d_fp"])
    for fid in [1,2,3]:
        for ztf_obj in ztf_objects:
            unique_days = count_days_for_filter(ztf_obj, fid)
            frame.loc[len(frame)] = [
                fid,
                len(unique_days["detections"]),
                max(unique_days["detections"]) - min(unique_days["detections"]) if unique_days["detections"] else 0,
                len(unique_days["non_detections"]),
                max(unique_days["non_detections"]) - min(unique_days["non_detections"]) if unique_days["non_detections"] else 0,
                len(unique_days["forced_photometry"]),
                max(unique_days["forced_photometry"]) - min(unique_days["forced_photometry"]) if unique_days["forced_photometry"] else 0,
            ]
    return frame

def print_statistics(lc_frame: pd.DataFrame):
    statistics = lc_frame.groupby("fid")[["n_det", "d_det", "n_non_det", "d_non_det", "n_fp", "d_fp"]].agg(["mean", "std"])
    print("Statistics of observations:")
    print(statistics)
    return statistics

def print_availability(lc_frame: pd.DataFrame):
    availability = lc_frame.groupby("fid")[["n_det", "n_non_det", "n_fp"]].agg(lambda x: (x > 0).sum() / len(x) * 100)
    print("Availability of observations:")
    print(availability)
    return availability

def _prepare_x(lc_frame: pd.DataFrame, columns: list, filter_0: bool = True):
    p95 = max(lc_frame[col].quantile(0.97) for col in columns)
    all_x = sorted(set().union(*[lc_frame[col].unique() for col in columns]))
    all_x = [x for x in all_x if x <= p95]
    if filter_0:
        all_x = [x for x in all_x if x > 0]
    return np.asarray(all_x)

def plot_observation_count(lc_frame: pd.DataFrame, fids=[1, 2, 3], filter_0: bool = True):

    fig, axes = plt.subplots(3, 1, figsize=(12, 15))
    columns = ["n_det", "n_non_det", "n_fp"]
    x = _prepare_x(lc_frame, columns, filter_0)

    for ax, col, title in zip(axes, columns, titles):

        for i, fid in enumerate(fids):
            counts = lc_frame[lc_frame["fid"] == fid][col].value_counts().reindex(x, fill_value=0)
            ax.bar(x + i * width, counts.values, width=width, label=f"fid {fid} ({fid_labels[fid]})", color=colors[i])

        step = 5
        ax.set_xticks(x[::step] + width)
        ax.set_xticklabels(x[::step])
        ax.set_xlabel("n days with at least one observation")
        ax.set_ylabel("n ztf objects")
        ax.set_title(title)
        ax.legend()

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4)
    plt.savefig(f"{os.path.dirname(os.path.abspath(__file__))}/observation_count.png", dpi=150, bbox_inches="tight")
    plt.show()

def plot_observation_span(lc_frame: pd.DataFrame, fids=[1, 2, 3], filter_0: bool = True):
    fig, axes = plt.subplots(3, 1, figsize=(12, 15))
    columns = ["d_det", "d_non_det", "d_fp"]
    x = _prepare_x(lc_frame, columns, filter_0)
    for ax, col, title in zip(axes, columns, titles):

        for i, fid in enumerate(fids):
            counts = lc_frame[lc_frame["fid"] == fid][col].value_counts().reindex(x, fill_value=0)
            ax.bar(x + i * width, counts.values, width=width, label=f"fid {fid} ({fid_labels[fid]})", color=colors[i])

        step = 25
        ax.set_xticks(x[::step] + width)
        ax.set_xticklabels(x[::step])
        ax.set_xlabel("observation span (days)")
        ax.set_ylabel("n ztf objects")
        ax.set_title(title)
        ax.legend()

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4)
    plt.savefig(f"{os.path.dirname(os.path.abspath(__file__))}/observation_span.png", dpi=150, bbox_inches="tight")
    plt.show()

M = LSSTMongoClient(uri="mongodb://localhost:27017", db_name="lsst-sn-type-analysis")
tuples: Tuple[TNSObject, ZTFObject] = M.get_tns_ztf_crossmatches()
ztf_objects = [t[1] for t in tuples]

frame = analyze_lc_timeseries(ztf_objects=ztf_objects)
print_statistics(lc_frame=frame)
print_availability(lc_frame=frame)
plot_observation_count(lc_frame=frame)
plot_observation_span(lc_frame=frame)

M.close()