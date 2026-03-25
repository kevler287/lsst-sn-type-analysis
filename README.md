# LSST Supernova Analysis

This project analyzes supernova data from the Rubin Observatory's LSST survey
to discover previously unknown features that discriminate between supernova types —
driven by the data itself rather than prior astrophysical assumptions.

Data is aggregated from multiple sources: photometric light curves and host galaxy
metadata from the Lasair alert broker, spectroscopic classifications from the
Transient Name Server (TNS), and auxiliary catalogues such as NED. All data is
stored locally in MongoDB for offline analysis.

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

## Next Steps

1. Get labeled data: According to my research the Transient Name Server (TNS) holds
the SN type for SN objects. This is the foundation of all analysis before starting
into LSST / ZTF data. Labeled data needs to be fetch and stored locally in MongoDB

2. Once this is done a connection between tns_name and diaObjectId
must be established to enrich the labeled TNS data with the surveys data.

3. Feature analysis:
- How much data can be gathered per SN type?
- Are there features which are available for most of the SN?
- Do they differ to the set of known features for SN type classification?
- Can SN objects without type class in TNS be classified?
- Can features from LSST which are probably not available for all labeled data
characterize SN type aswell?
