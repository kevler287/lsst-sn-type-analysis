from pydantic import BaseModel, Field
from typing import Optional

class DiaSource(BaseModel):
    diaSourceId: int
    isForced: bool = Field(description="Whether this source was detected automatically or forced at a known position")
    midpointMjdTai: float = Field(description="Effective mid-visit time for this diaSource, expressed as Modified Julian Date, International Atomic Time")
    ra: float
    decl: float
    detector: int
    band: str = Field(description="Filter band this source was observed with")
    psfFlux: float = Field(description="PSF weighted sum of all pixel values inside the aperture radius")
    psfFluxErr: float = Field(description="Estimated uncertainty of psfFlux")
    scienceFlux: float
    scienceFluxErr: float
    timeProcessedMjdTai: float
    timeWithdrawnMjdTai: Optional[float] = None
    visit: int

    #____________________BELOW IS ONLY SET WHEN isForced=False_________________________________
    
    # Aperture flux fields: Brightness measured by summing all pixel values within a fixed circular
    # radius ("aperture") around the source position. Simpler than PSF fitting but less precise for
    # point sources. Units are nJy. Compare with psfFlux which fits the telescope's PSF profile
    # instead — psfFlux is generally preferred for point-like sources such as distant supernovae.
    apFlux: Optional[float] = Field(default=None, description="sum of all pixel values inside the aperture radius")
    apFluxErr: Optional[float] = Field(default=None, description="Estimated uncertainty of apFlux")
    apFlux_flag: Optional[bool] = Field(default=None, description="General aperture flux algorithm failure flag; set if anything went wrong when measuring aperture fluxes")
    apFlux_flag_apertureTruncated: Optional[bool] = Field(default=None, description="Aperture is cutoff by the edge of the image")

    bboxSize: Optional[int] = Field(default=None, description="Size of the square bounding box in pixels")
    centroid_flag: Optional[bool] = Field(default=None, description="General centroid algorithm failure flag; set if anything went wrong when fitting the centroid")

    # Position
    raErr: Optional[float] = None
    decErr: Optional[float] = None
    ra_dec_Cov: Optional[float] = None

    # Dipole fields: In difference images, a source can appear as a dipole — a positive and negative
    # blob side by side. This occurs when a source has moved between the template and science image
    # (e.g. an asteroid) or when the alignment between the two images was imperfect.
    # For supernovae, these fields are typically null/false. A isDipole=True for an SN candidate
    # is a warning sign of a reduction artifact.
    dipoleAngle: Optional[float] = None
    dipoleChi2: Optional[float] = None
    dipoleFitAttempted: Optional[bool] = None
    dipoleFluxDiff: Optional[float] = None
    dipoleFluxDiffErr: Optional[float] = None
    dipoleLength: Optional[float] = None
    dipoleMeanFlux: Optional[float] = None
    dipoleMeanFluxErr: Optional[float] = None
    dipoleNdata: Optional[int] = None

    extendedness: Optional[float] = Field(default=None, description="0 means perfect point shaped object, 1 mean extended e.g. galaxy")

    # Forced PSF flux flags: Unlike normal detection where the algorithm searches for sources
    # automatically, forced PSF photometry fits the PSF at a fixed, pre-known position regardless
    # of whether a source is visibly detected there. This is critical for building complete light
    # curves — it allows flux measurements even in epochs where the supernova is too faint to be
    # detected automatically. These flags indicate problems with that forced measurement
    forced_PsfFlux_flag: Optional[bool] = Field(default=None, description="Indicates if PSF fit suceeded or not")
    forced_PsfFlux_flag_edge: Optional[bool] = Field(default=None, description="Indicates if object is to close to the edge")
    forced_PsfFlux_flag_noGoodPixels: Optional[bool] = Field(default=None, description="Indicates if object is masked")

    glint_trail: Optional[bool] = None
    isDipole: Optional[bool] = None
    isNegative: Optional[bool] = None

    # Shape moments
    ixx: Optional[float] = None
    ixxPSF: Optional[float] = None
    ixy: Optional[float] = None
    ixyPSF: Optional[float] = None
    iyy: Optional[float] = None
    iyyPSF: Optional[float] = None

    parentDiaSourceId: Optional[int] = None

    # Pixel flags
    pixelFlags: Optional[bool] = None
    pixelFlags_bad: Optional[bool] = None
    pixelFlags_cr: Optional[bool] = None
    pixelFlags_crCenter: Optional[bool] = None
    pixelFlags_edge: Optional[bool] = None
    pixelFlags_injected: Optional[bool] = None
    pixelFlags_injectedCenter: Optional[bool] = None
    pixelFlags_injected_template: Optional[bool] = None
    pixelFlags_injected_templateCenter: Optional[bool] = None
    pixelFlags_interpolated: Optional[bool] = None
    pixelFlags_interpolatedCenter: Optional[bool] = None
    pixelFlags_nodata: Optional[bool] = None
    pixelFlags_nodataCenter: Optional[bool] = None
    pixelFlags_offimage: Optional[bool] = None
    pixelFlags_saturated: Optional[bool] = None
    pixelFlags_saturatedCenter: Optional[bool] = None
    pixelFlags_streak: Optional[bool] = None
    pixelFlags_streakCenter: Optional[bool] = None
    pixelFlags_suspect: Optional[bool] = None
    pixelFlags_suspectCenter: Optional[bool] = None

    # PSF flux
    psfChi2: Optional[float] = None
    psfFlux_flag: Optional[bool] = None
    psfFlux_flag_edge: Optional[bool] = None
    psfFlux_flag_noGoodPixels: Optional[bool] = None
    psfLnL: Optional[float] = None
    psfNdata: Optional[int] = None

    reliability: Optional[float] = None

    # Science / template flux
    templateFlux: Optional[float] = None
    templateFluxErr: Optional[float] = None

    # Shape flags
    shape_flag: Optional[bool] = None
    shape_flag_no_pixels: Optional[bool] = None
    shape_flag_not_contained: Optional[bool] = None
    shape_flag_parent_source: Optional[bool] = None

    snr: Optional[float] = None
    ssObjectId: Optional[int] = None

    # Trail fields
    trailAngle: Optional[float] = None
    trailAngleErr: Optional[float] = None
    trailChi2: Optional[float] = None
    trailDec: Optional[float] = None
    trailDecErr: Optional[float] = None
    trailFlux: Optional[float] = None
    trailFluxErr: Optional[float] = None
    trailLength: Optional[float] = None
    trailLengthErr: Optional[float] = None
    trailNdata: Optional[int] = None
    trailRa: Optional[float] = None
    trailRaErr: Optional[float] = None
    trail_flag_edge: Optional[bool] = None

    # Pixel coordinates
    x: Optional[float] = None
    xErr: Optional[float] = None
    y: Optional[float] = None
    yErr: Optional[float] = None