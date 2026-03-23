from pydantic import BaseModel
from typing import List
from models.dia_source import DiaSource
from models.sherlock_classification import SherlockClassification
from pydantic import BaseModel, Field
from typing import Optional, List

class Annotation(BaseModel):
    topic: Optional[str] = Field(None, description="Classifier identifier, e.g. 'r0b_lvra'.")
    classification: Optional[str] = Field(None, description="Classifier score, typically a probability between 0 and 1.")

class DiaObject(BaseModel):
    diaObjectId: int = Field(..., description="Unique identifier for this DIA object.")
    sources: List[DiaSource] = Field(default_factory=list, description="List of DIA sources associated with this object.")
    sherlock: SherlockClassification = Field(..., description="Sherlock classification data for this object.")
    annotations: List[Annotation] = Field(default_factory=list, description="List of annotations for this object.")

    # Brightness
    absMag: Optional[float] = Field(None, description="Absolute magnitude at absMagMJD. A key discriminator between SN types: Ia peaks around -19.3, II around -17.")

    # Blackbody bolometric fit — a blackbody spectrum is fitted to the available band
    # measurements to estimate the total luminosity across all wavelengths. More physically
    # meaningful than single-band magnitudes but requires at least 2-3 band detections.
    # Often null when insufficient multi-band coverage is available.
    BBBRiseRate: Optional[float] = Field(None, description="Rise rate of the bolometric light curve fit. Strong discriminator between SN types if available.")
    BBBFallRate: Optional[float] = Field(None, description="Fall rate of the bolometric light curve fit.")
    BBBTemp: Optional[float] = Field(None, description="Blackbody temperature in Kelvin derived from multi-band photometry.")
    BBBPeakAbsMag: Optional[float] = Field(None, description="Absolute magnitude at peak from bolometric fit. More reliable than absMag if available.")
    BBBPeakMJD: Optional[float] = Field(None, description="MJD of the bolometric peak.")

    # Galactic / extinction
    ebv: Optional[float] = Field(None, description="Milky Way dust extinction along the line of sight (E(B-V)). Should be used to correct observed magnitudes before analysis.")
    glat: Optional[float] = Field(None, description="Galactic latitude in degrees. Objects near 0 are close to the Milky Way plane and may suffer from higher extinction and source confusion.")

    # TNS
    tns_name: Optional[str] = Field(None, description="Transient Name Server identifier (e.g. SN2026abc). If set, a spectroscopic classification may be available and can be used as a training label.")

    def get_sorted_sources(self):
        return sorted(self.sources, key=lambda source: source.midpointMjdTai)

    @classmethod
    def from_dict(cls, data):
        sources: List[DiaSource] = []

        for source_dict in data['diaSourcesList']:
            source = DiaSource(
                isForced=False,
                **source_dict
            )
            sources.append(source)

        for source_dict in data['diaForcedSourcesList']:
            source = DiaSource(
                diaSourceId=source_dict['diaForcedSourceId'],
                isForced=True,
                **source_dict
            )
            sources.append(source)

        lasair_data = data.get('lasairData', {})
        return cls(
            **lasair_data,
            sources=sources
        )
