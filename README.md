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
The light curve shows a characteristic plateau of around 100 days after peak before dropping
sharply — a strong discriminator in our data. Fainter than Ia at peak (around -17 mag on
average) and more variable. Found exclusively in star-forming galaxies, often in
spiral arms where young massive stars are concentrated.

### Type Ib/Ic — Stripped Core Collapse
Like Type II but the progenitor lost its outer layers before exploding. No plateau
in the light curve — instead a faster, smoother decline similar to Ia but typically
fainter and more irregular. Ib and Ic are difficult to distinguish photometrically
without spectra. Like Type II, they only occur in star-forming environments, which
makes host galaxy properties a potential discriminator against Type Ia.

## Steps

### 1. Get labeled data from TNS
According to my research the Transient Name Server (TNS) holds
the SN type for SN objects. This is the foundation of all analysis before starting
into LSST / ZTF data. Labeled data needs to be fetch and stored locally in MongoDB.

Last update: 2026-03-25

| SN Type | Count |
|---|---:|
| SN Ia | 12173 |
| SN II | 2935 |
| SN IIn | 524 |
| SN Ia-91T-like | 470 |
| SN Ic | 409 |
| SN Ib | 325 |
| SN IIP | 313 |
| SN IIb | 294 |
| SLSN-I | 217 |
| SN Ic-BL | 177 |
| SN Ia-91bg-like | 162 |
| SLSN-II | 114 |
| SN Ia-pec | 99 |
| SN | 87 |
| SN Ib/c | 82 |
| SN Ibn | 71 |
| SN Iax[02cx-like] | 63 |
| SN I | 60 |
| SN Ia-CSM | 43 |
| SN Ib-pec | 17 |
| SN Ia-SC | 17 |
| SN II-pec | 16 |
| SN Ib-Ca-rich | 12 |
| SN Icn | 7 |
| SN IIn-pec | 5 |
| SN IIL | 3 |
| SN Ic-pec | 3 |
| SN Ibn/Icn | 2 |
| SN Ia-Ca-rich | 1 |
| SN Ic-Ca-rich | 1 |
| SN Ien | 1 |
| **Total** | **18703** |

> **_NOTE:_** Well, TNS seems to be very specific with the SN types. I don't know if I will group them later on or leave as is.

### 2. Build connection between TNS data and survey data
Once this is done a connection between TNS entry and survey entries must be established to enrich the labeled TNS data with the surveys data. Survey entries are pulled from Lasair LSST broker and ALeRCE broker. From Lasair broker almost 140k of classifed SNe were pulled but only few are metnioned in TNS yet. From ALeRCE broker all the ZTF objects metnioned in tns.internal_names were pulled and stored locally in MongoDB.

Last update: 2026-03-25

| SN Type | TNS Count | ZTF Count (ALeRCE) | LSST Count (Lasair) |
|---|---|---|---:|
|SN Ia|12173|5836|17|6331|
|SN II|2935|1449|5|1483|
|SN IIn|524|243|1|280|
|SN Ia-91T-like|470|200|1|270|
|SN Ic|409|174|1|235|
|SN Ib|325|154|0|171|
|SN IIP|313|111|0|202|
|SN IIb|294|151|0|143|
|SLSN-I|217|124|0|93|
|SN Ic-BL|177|85|0|92|
|SN Ia-91bg-like|162|73|0|89|
|SLSN-II|114|57|0|57|
|SN Ia-pec|99|44|0|55|
|SN|87|39|0|48|
|SN Ib/c|82|40|0|42|
|SN Ibn|71|36|0|35|
|SN Iax[02cx-like]|63|31|0|32|
|SN I|60|29|1|31|
|SN Ia-CSM|43|25|0|18|
|SN Ia-SC|17|15|0|2|
|SN Ib-pec|17|8|0|9|
|SN II-pec|16|11|0|5|
|SN Ib-Ca-rich|12|9|0|3|
|SN Icn|7|6|0|1|
|SN IIn-pec|5|2|0|3|
|SN Ic-pec|3|1|0|2|
|SN IIL|3|0|0|3|
|SN Ibn/Icn|2|2|0|0|
|SN Ien|1|1|0|0|
|SN Ia-Ca-rich|1|1|0|0|
|SN Ic-Ca-rich|1|1|0|0|

### 3. Feature analysis

> **_NOTE:_** since this is not straight forward I decided to create a diary kind of. Check notes.md files in ./diary/ for further details.