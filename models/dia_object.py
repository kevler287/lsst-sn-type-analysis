from pydantic import BaseModel
from typing import List
from models.dia_source import DiaSource
from pydantic import BaseModel, Field
from typing import Optional, List

class DiaObject(BaseModel):
    diaObjectId: int = Field(..., alias="_id", description="Unique identifier for this DIA object.")
    class_id: int = Field(..., description="Class ID for the object.")
    probability: float = Field(..., description="Probability of the classification.")

    sources: List[DiaSource] = Field(default_factory=list, description="List of DIA sources associated with this object.")

    # # Brightness
    # absMag: Optional[float] = Field(None, description="Absolute magnitude at absMagMJD. A key discriminator between SN types: Ia peaks around -19.3, II around -17.")

    # # Blackbody bolometric fit — a blackbody spectrum is fitted to the available band
    # # measurements to estimate the total luminosity across all wavelengths. More physically
    # # meaningful than single-band magnitudes but requires at least 2-3 band detections.
    # # Often null when insufficient multi-band coverage is available.
    # BBBRiseRate: Optional[float] = Field(None, description="Rise rate of the bolometric light curve fit. Strong discriminator between SN types if available.")
    # BBBFallRate: Optional[float] = Field(None, description="Fall rate of the bolometric light curve fit.")
    # BBBTemp: Optional[float] = Field(None, description="Blackbody temperature in Kelvin derived from multi-band photometry.")
    # BBBPeakAbsMag: Optional[float] = Field(None, description="Absolute magnitude at peak from bolometric fit. More reliable than absMag if available.")
    # BBBPeakMJD: Optional[float] = Field(None, description="MJD of the bolometric peak.")

    # # Galactic / extinction
    # ebv: Optional[float] = Field(None, description="Milky Way dust extinction along the line of sight (E(B-V)). Should be used to correct observed magnitudes before analysis.")
    # glat: Optional[float] = Field(None, description="Galactic latitude in degrees. Objects near 0 are close to the Milky Way plane and may suffer from higher extinction and source confusion.")

    # # TNS
    # tns_name: Optional[str] = Field(None, description="Transient Name Server identifier (e.g. SN2026abc). If set, a spectroscopic classification may be available and can be used as a training label.")

    model_config = {"populate_by_name": True}
