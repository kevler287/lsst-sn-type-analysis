from pydantic import BaseModel, Field
from typing import Optional, Any

class DiaSource(BaseModel):
    diaSourceId: int = Field(description="diaSourceId or diaForcedSourceId")
    isForced: bool = Field(description="Whether this source was detected automatically or forced at a known position")
    midpointMjdTai: float = Field(description="Effective mid-visit time for this diaSource, expressed as Modified Julian Date, International Atomic Time")
    ra: float
    decl: float
    detector: int
    band: Any = Field(description="Filter band this source was observed with")
    psfFlux: float = Field(description="PSF weighted sum of all pixel values inside the aperture radius")
    psfFluxErr: float = Field(description="Estimated uncertainty of psfFlux")
    scienceFlux: float
    scienceFluxErr: float
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

    # Forced PSF flux flags: Unlike normal detection where the algorithm searches for sources
    # automatically, forced PSF photometry fits the PSF at a fixed, pre-known position regardless
    # of whether a source is visibly detected there. This is critical for building complete light
    # curves — it allows flux measurements even in epochs where the supernova is too faint to be
    # detected automatically. These flags indicate problems with that forced measurement
    forced_PsfFlux_flag: Optional[bool] = Field(default=None, description="Indicates if PSF fit suceeded or not")
    forced_PsfFlux_flag_edge: Optional[bool] = Field(default=None, description="Indicates if object is to close to the edge")
    forced_PsfFlux_flag_noGoodPixels: Optional[bool] = Field(default=None, description="Indicates if object is masked")

    glint_trail: Optional[bool] = Field(default=None, description="Indicates if optical noise is present in the image")
    isDipole: Optional[bool] = Field(default=None, description="Indicates if alignment failed. see above")
    isNegative: Optional[bool] = Field(default=None, description="Indicates if template image was lighter than science image")

    # Shape moments: Second-order moments describing the source's light distribution as an
    # ellipse. ixx/iyy capture the extent along x/y, ixy the diagonal covariance (tilt).
    # Like a fisheye lens, the telescope's optics distort point sources depending on their
    # position on the detector — a point source in the corner looks different than one in
    # the center. The PSF variants (ixxPSF, iyyPSF, ixyPSF) capture exactly this expected
    # distortion at the source's specific detector position, serving as a reference for what
    # a perfect point source should look like there. Neither the source moments nor the PSF
    # moments are meaningful in isolation — only their ratio reveals the true shape of the
    # source, which is summarized by the extendedness parameter (0 = point-like SN, 1 = galaxy).
    ixx: Optional[float] = Field(default=None, description="Extension along x axis")
    ixy: Optional[float] = Field(default=None, description="Diagonal extension")
    iyy: Optional[float] = Field(default=None, description="Extension along y axis")
    ixxPSF: Optional[float] = Field(default=None, description="Expected extension along x axis")
    ixyPSF: Optional[float] = Field(default=None, description="Expected diagonal extension")
    iyyPSF: Optional[float] = Field(default=None, description="Expected extension along y axis")
    extendedness: Optional[float] = Field(default=None, description="= f(ixx/ixxPSF, iyy/iyyPSF, ixy/ixyPSF)")

    parentDiaSourceId: Optional[int] = Field(default=None, description="If two sources are detected as one and split later, this field links them")

    # Pixel flags indicate problematic pixels
    pixelFlags: Optional[bool] = Field(default=None, description="overall flag")
    pixelFlags_bad: Optional[bool] = Field(default=None, description="permanent defect pixels (hardware issue)")
    pixelFlags_cr: Optional[bool] = Field(default=None, description="cosmic ray can cause pixels to appear like point sources")
    pixelFlags_crCenter: Optional[bool] = Field(default=None, description="cosmic ray can cause pixels to appear like point sources in center")
    pixelFlags_edge: Optional[bool] = Field(default=None, description="source to close to the detector edge")
    pixelFlags_injected: Optional[bool] = Field(default=None, description="indicates atrificial injection of a source. if set ignore for SN foreshadowing")
    pixelFlags_injectedCenter: Optional[bool] = None
    pixelFlags_injected_template: Optional[bool] = Field(default=None, description="indicates atrificial injection of a source in template. if set ignore for SN foreshadowing")
    pixelFlags_injected_templateCenter: Optional[bool] = None
    pixelFlags_interpolated: Optional[bool] = Field(default=None, description="defected pixel was reconstructed")
    pixelFlags_interpolatedCenter: Optional[bool] = Field(default=None, description="defected pixel was reconstructed in center")
    pixelFlags_nodata: Optional[bool] = Field(default=None, description="no data")
    pixelFlags_nodataCenter: Optional[bool] = Field(default=None, description="no data in center")
    pixelFlags_offimage: Optional[bool] = Field(default=None, description="source is cutoff")
    pixelFlags_saturated: Optional[bool] = Field(default=None, description="pixel was saturated. real flux is higher")
    pixelFlags_saturatedCenter: Optional[bool] = Field(default=None, description="pixel was saturated in center. real flux is higher")
    pixelFlags_streak: Optional[bool] = Field(default=None, description="some satellite trail is visible in the image")
    pixelFlags_streakCenter: Optional[bool] = Field(default=None, description="some satellite trail is visible in the center of image")
    pixelFlags_suspect: Optional[bool] = Field(default=None, description="pixel is close to be saturated. not reliable")
    pixelFlags_suspectCenter: Optional[bool] = Field(default=None, description="pixel in center is close to be saturated. not reliable")

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

    @classmethod
    def from_alerce(cls, data: dict, is_forced: bool) -> 'DiaSource':
        return cls(
            diaSourceId=data.get("measurement_id"),
            isForced=is_forced,
            midpointMjdTai=data.get("mjd"),
            decl=data.get("dec"),
            **data
        )