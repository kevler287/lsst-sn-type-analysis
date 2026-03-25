from typing import Optional, List, Dict, ClassVar, Any
from datetime import datetime
from pydantic import BaseModel, Field, model_validator


class BandData(BaseModel):
    psfFlux: Optional[float] = Field(None, description="Latest PSF flux measurement for this band")
    latestMJD: Optional[float] = Field(None, description="MJD of the latest observation in this band")
    psfFluxMean: Optional[float] = Field(None, description="Mean PSF flux over all detections")
    psfFluxMeanErr: Optional[float] = Field(None, description="Error on the mean PSF flux")

    psfFluxSigma: Optional[float] = Field(None, description="Standard deviation of PSF flux measurements")
    psfFluxNdata: int = Field(..., description="Number of PSF flux data points")

    fpFluxMean: Optional[float] = Field(None, description="Mean forced photometry flux")
    fpFluxMeanErr: Optional[float] = Field(None, description="Error on forced photometry mean flux")

    scienceFluxMean: Optional[float] = Field(None, description="Mean science image flux")
    scienceFluxMeanErr: Optional[float] = Field(None, description="Error on science flux mean")

    psfFluxMin: Optional[float] = Field(None, description="Minimum observed PSF flux")
    psfFluxMax: Optional[float] = Field(None, description="Maximum observed PSF flux")
    psfFluxMaxSlope: Optional[float] = Field(None, description="Maximum rate of change in PSF flux")
    psfFluxErrMean: Optional[float] = Field(None, description="Mean error of PSF flux measurements")


class LasairObject(BaseModel):
    # --- Identity ---
    diaObjectId: int = Field(..., alias="_id", description="Unique DIA object identifier")
    ra: float = Field(..., description="Right ascension in degrees (J2000)")
    decl: float = Field(..., description="Declination in degrees (J2000)")

    # --- Temporal ---
    firstDiaSourceMjdTai: float = Field(..., description="MJD of first DIA source detection")
    lastDiaSourceMjdTai: float = Field(..., description="MJD of most recent DIA source detection")
    timestamp: Optional[str] = Field(None, description="ISO timestamp of last database update")

    # --- Summary Photometry ---
    latest_psfFlux: Optional[float] = Field(None, description="Most recent PSF flux across all bands")
    absMag: Optional[float] = Field(None, description="Absolute magnitude at peak")
    absMagMJD: Optional[float] = Field(None, description="MJD at which absMag was measured")

    # --- Per-Band Data ---
    u_band: BandData = Field(..., description="u-band photometric data")
    g_band: BandData = Field(..., description="g-band photometric data")
    r_band: BandData = Field(..., description="r-band photometric data")
    i_band: BandData = Field(..., description="i-band photometric data")
    z_band: BandData = Field(..., description="z-band photometric data")
    y_band: BandData = Field(..., description="y-band photometric data")

    # --- Sky & Dust ---
    glat: Optional[float] = Field(None, description="Galactic latitude in degrees")
    ebv: Optional[float] = Field(None, description="E(B-V) dust extinction")

    # --- Blackbody Fit ---
    BBBRiseRate: Optional[float] = Field(None, description="Blackbody fit rise rate")
    BBBFallRate: Optional[float] = Field(None, description="Blackbody fit fall rate")
    BBBTemp: Optional[float] = Field(None, description="Blackbody fit temperature")
    BBBPeakFlux: Optional[float] = Field(None, description="Blackbody fit peak flux")
    BBBPeakMJD: Optional[float] = Field(None, description="MJD of blackbody fit peak")
    BBBPeakAbsMag: Optional[float] = Field(None, description="Absolute magnitude at blackbody fit peak")

    # --- Sherlock Host Association ---
    classification: Optional[str] = Field(None, description="Sherlock classification (e.g. SN, AGN, VS)")
    catalogue_table_name: Optional[str] = Field(None, description="Source catalogue name (e.g. NED, SDSS)")
    catalogue_object_id: Optional[str] = Field(None, description="ID of the associated object in the catalogue")
    catalogue_object_type: Optional[str] = Field(None, description="Type of the associated catalogue object")
    separationArcsec: Optional[float] = Field(None, description="Angular separation from host in arcseconds")
    physical_separation_kpc: Optional[float] = Field(None, description="Physical separation from host in kpc")
    direct_distance: Optional[float] = Field(None, description="Direct distance measurement if available")
    distance: Optional[float] = Field(None, description="Distance to host in Mpc")
    redshift: Optional[float] = Field(None, alias="z", description="Spectroscopic redshift of the host")
    photoZ: Optional[float] = Field(None, description="Photometric redshift of the host")
    photoZErr: Optional[float] = Field(None, description="Error on the photometric redshift")
    Mag: Optional[float] = Field(None, description="Magnitude of the host galaxy")
    MagFilter: Optional[str] = Field(None, description="Filter used for host magnitude")
    MagErr: Optional[float] = Field(None, description="Error on the host magnitude")
    classificationReliability: Optional[int] = Field(None, description="Reliability score of the classification (1=confident, 2=possible)")

    # --- TNS ---
    tns_name: Optional[str] = Field(None, description="Transient Name Server name if reported")

    model_config = {"populate_by_name": True}

    # --- Validator ---
    @model_validator(mode="before")
    @classmethod
    def extract_band_data(cls, data: dict) -> dict:
        if "z" in data and not isinstance(data["z"], dict):
            data["redshift"] = data.pop("z")
        
        for band in ("u", "g", "r", "i", "z", "y"):
            band_dict = {}
            for field in BandData.model_fields:
                key = f"{band}_{field}"
                band_dict[field] = data.pop(key, None)
            if band_dict.get("psfFluxNdata") is None:
                band_dict["psfFluxNdata"] = 0
            data[f"{band}_band"] = band_dict
        return data