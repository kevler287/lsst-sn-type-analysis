# Day 1 — Getting Familiar with the Data

## Goal

First contact with the dataset. No pressure on performance today — the goal is to understand the data, build a minimal feature vector, and get a first classifier running to see where we stand.

## Dataset

- Source: ZTF photometry cross-matched with TNS labels
- Total objects after cross-match: 8998
- Filtered to three upper-level classes: **Ia**, **II**, **Ib/c**

**Class distribution after grouping:**

| Class | Count |
|---|---:|
| Ia | 6296 |
| II | 2053 |
| Ib/c | 649 |

Class imbalance is significant and will need to be addressed.

## Feature Vector (v1)

Scalar features only — no time series. Only detections are used for computing the features. Need to figure out how to make use of non-detections and forced photometry. Guess I need more background knowledge for this.

```
g_max_magpsf       — peak brightness in g-band
g_rise_time        — days from first detection to peak (g)
g_dm15             — magnitude decline 15 days after peak (g)

r_max_magpsf       — peak brightness in r-band
r_rise_time        — days from first detection to peak (r)
r_dm15             — magnitude decline 15 days after peak (r)

g_r_at_peak        — g-r color at time of g-band peak
g_r_at_10d         — g-r color at peak+10 days
g_r_at_20d         — g-r color at peak+20 days
g_r_peak_lag       — days between g-band and r-band peak

corrected          — whether host-subtraction was applied (binary)
stellar            — whether the object is morphologically classified as a point source
```

## Model

Starting simple: **XGBoost** — handles NaN natively, supports sample weights for class imbalance

## Results

### Classification Report

| Class | Precision | Recall | F1 |
|---|---|---|---|
| SN Ia | 0.83 | 0.94 | 0.88 |
| SN II | 0.72 | 0.58 | 0.64 |
| SN Ib/c | 0.40 | 0.13 | 0.20 |

### Interpretation

Not good (obviously) - Class imbalance does its work but nothing we can do about it except weighting which was already applied.
So we need to adjust somewhere else:
- feature analysis (how many NaN for features?)
- lightcurve analysis (do all show the same pattern or some are cutoff?)
- make use of non-detections & forced photometry
