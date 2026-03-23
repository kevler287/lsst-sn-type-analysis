# LSST Supernova Analysis

This project explores supernova data from the Rubin Observatory's LSST survey
to characterize different supernova types and build a classification pipeline —
driven by the data itself rather than prior astrophysical assumptions.

The core idea is simple: given photometric light curves and host galaxy metadata
from Lasair's alert broker, can we let statistics and machine learning reveal
which parameters actually matter for distinguishing supernova types? Feature
importance, clustering, and supervised classification will guide the analysis
rather than hand-picked domain knowledge.

The project is structured in three phases:

1. **Exploration** — get a feel for the data, its coverage, quality, and limitations
2. **Characterization** — identify which features discriminate between SN types
3. **Classification** — build and evaluate a classifier on labeled TNS objects

A potential fourth phase extends the analysis to host galaxy properties,
investigating whether galaxy characteristics correlate with supernova type.

Data is sourced from the Lasair LSST alert broker and stored locally in MongoDB.

## Supernova Types

### Type Ia — Thermonuclear Supernova
A white dwarf accretes mass from a companion star until it explodes. The key property
for our analysis is their remarkable consistency: peak absolute magnitude is always
around -19.3 mag, rise time ~15-20 days, and the light curve follows a predictable
decline. In multi-band photometry, the color evolves from blue to red after peak.
No hydrogen in the spectrum. They occur in all galaxy types, including ellipticals
with no ongoing star formation.

### Type II — Core Collapse with Hydrogen
A massive star collapses and explodes, leaving a neutron star or black hole behind.
The light curve shows a characteristic plateau of ~100 days after peak before dropping
sharply — a strong discriminator in our data. Fainter than Ia at peak (~-17 mag on
average) and more variable. Found exclusively in star-forming galaxies, often in
spiral arms where young massive stars are concentrated.

### Type Ib/Ic — Stripped Core Collapse
Like Type II but the progenitor lost its outer layers before exploding. No plateau
in the light curve — instead a faster, smoother decline similar to Ia but typically
fainter and more irregular. Ib and Ic are difficult to distinguish photometrically
without spectra. Like Type II, they only occur in star-forming environments, which
makes host galaxy properties a potential discriminator against Type Ia.