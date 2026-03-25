import matplotlib.pyplot as plt
from archive.dia_object import DiaObject

def plot_light_curve(obj: DiaObject) -> None:
    sources = sorted(obj.sources, key=lambda s: s.midpointMjdTai)
    bands = sorted(set(s.band for s in sources))
    colors = {"u": "purple", "g": "green", "r": "red", "i": "orange", "z": "brown", "y": "black"}

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
    fig.suptitle(f"Light Curve — diaObjectId: {obj.diaObjectId}", fontsize=14)

    for ax, is_forced, title in [
        (ax1, False, "Detected Sources"),
        (ax2, True,  "Forced Sources"),
    ]:
        for band in bands:
            band_sources = [s for s in sources if s.band == band and s.isForced == is_forced]
            if not band_sources:
                continue
            mjd     = [s.midpointMjdTai for s in band_sources]
            flux    = [s.psfFlux for s in band_sources]
            fluxerr = [s.psfFluxErr for s in band_sources]
            ax.errorbar(mjd, flux, yerr=fluxerr, fmt="o-", capsize=4,
                        color=colors.get(band, "gray"), label=band)

        ax.set_title(title)
        ax.set_ylabel("psfFlux (nJy)")
        ax.legend(title="Band")
        ax.grid(True, alpha=0.3)

    ax2.set_xlabel("MJD (TAI)")
    plt.tight_layout()
    plt.show()