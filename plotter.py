import requests
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import ZScaleInterval
from io import BytesIO
import time
from models.sn_object import SuperNovaDiaObject

def load_fits_image(url: str):
    time.sleep(1)
    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
        with fits.open(BytesIO(response.content), ignore_missing_end=True) as hdul:
            return hdul[0].data
    except Exception:
        return None

def plot_object(obj: SuperNovaDiaObject):
    sources = obj.sources
    n = len(sources)
    
    fig, axes = plt.subplots(n, 3, figsize=(9, 3 * n))
    fig.suptitle(f"diaObjectId: {obj.diaObjectId}", fontsize=14)

    # Spaltenüberschriften
    for ax, title in zip(axes[0], ["Science", "Template", "Difference"]):
        ax.set_title(title, fontsize=12)

    interval = ZScaleInterval()

    for row, source in enumerate(sources):
        images = [
            load_fits_image(source.ScienceUrl),
            load_fits_image(source.TemplateUrl),
            load_fits_image(source.DifferenceUrl),
        ]
        for col, data in enumerate(images):
            ax = axes[row, col]
            if data is None:
                ax.text(0.5, 0.5, "N/A", ha="center", va="center", transform=ax.transAxes)
                ax.set_facecolor("black")
            else:
                vmin, vmax = interval.get_limits(data)
                ax.imshow(data, cmap="gray", origin="lower", vmin=vmin, vmax=vmax)
            ax.set_xticks([])
            ax.set_yticks([])
        print(f"Plotting source {source.diaSourceId}")

    plt.tight_layout()
    plt.show()