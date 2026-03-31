from typing import Optional, List, Dict
from pydantic import BaseModel, Field
import numpy as np

class ZTFNonDetection(BaseModel):
    mjd: float = Field(..., description="Modified Julian Date of observation")
    fid: int = Field(..., description="Filter ID (1=g, 2=r, 3=i)")
    diffmaglim: float = Field(..., description="5-sigma limiting magnitude of difference image")

class ZTFDetection(BaseModel):
    candid: str = Field(..., description="Unique candidate identifier")
    mjd: float = Field(..., description="Modified Julian Date of observation")
    fid: int = Field(..., description="Filter ID (1=g, 2=r, 3=i)")

    magpsf: float = Field(..., description="PSF-fit magnitude")
    sigmapsf: float = Field(..., description="Error on PSF-fit magnitude")
    magap: float = Field(..., description="Aperture magnitude (small)")
    sigmagap: float = Field(..., description="Error on small aperture magnitude")
    diffmaglim: float = Field(..., description="5-sigma limiting magnitude of difference image")

    distnr: float = Field(..., description="Distance to nearest source in arcseconds")

    rb: float = Field(..., description="Real/bogus score (0=bogus, 1=real)")
    isdiffpos: int = Field(..., description="Whether the difference is positive (1) or negative (-1)")
    phase: float = Field(..., description="Phase of the detection")
    corrected: bool = Field(..., description="Whether photometry has been host-subtraction corrected")
    dubious: bool = Field(..., description="Whether this detection is flagged as dubious")

class ZTFForcedPhotometry(BaseModel):
    candid: str = Field(..., description="Unique candidate identifier")
    mjd: float = Field(..., description="Modified Julian Date of observation")
    fid: int = Field(..., description="Filter ID (1=g, 2=r, 3=i)")

    # --- Photometry ---
    mag: float = Field(..., description="Forced PSF magnitude")
    e_mag: float = Field(..., description="Error on forced PSF magnitude")
    mag_corr: Optional[float] = Field(None, description="Host-corrected magnitude")
    e_mag_corr: Optional[float] = Field(None, description="Error on host-corrected magnitude")
    diffmaglim: float = Field(..., description="5-sigma limiting magnitude of difference image")

    # --- Flags ---
    isdiffpos: int = Field(..., description="Whether the difference is positive (1) or negative (-1)")
    corrected: bool = Field(..., description="Whether photometry has been host-subtraction corrected")
    dubious: bool = Field(..., description="Whether this detection is flagged as dubious")
    procstatus: str = Field(..., description="Processing status code (0=good)")

class ZTFObject(BaseModel):
    # --- Identity ---
    oid: str = Field(..., alias="_id", description="ZTF object identifier")

    # --- Current Detection Stats ---
    ndet: int = Field(..., description="Number of detections in current dataset")
    firstmjd: float = Field(..., description="MJD of first detection")
    lastmjd: float = Field(..., description="MJD of last detection")
    deltajd: float = Field(..., description="Time baseline between first and last detection in days")

    # --- Position ---
    meanra: float = Field(..., description="Mean right ascension in degrees")
    meandec: float = Field(..., description="Mean declination in degrees")

    # --- Photometry ---
    g_r_max: Optional[float] = Field(None, description="Maximum g-r colour index")
    g_r_mean: Optional[float] = Field(None, description="Mean g-r colour index")

    # --- Flags ---
    corrected: bool = Field(..., description="Whether photometry has been corrected")
    stellar: bool = Field(..., description="Whether the object is classified as stellar")

    detections: List[ZTFDetection] = Field(default_factory=list, description="List of ZTF detections for this object")
    non_detections: List[ZTFNonDetection] = Field(default_factory=list, description="List of ZTF non-detections for this object")
    forced_photometry: List[ZTFForcedPhotometry] = Field(default_factory=list, description="List of ZTF forced photometry for this object")

    model_config = {"populate_by_name": True}

    def count_filter_ids(self, detections_list: list) -> dict:
        filter_ids = {
            1: 0,
            2: 0,
            3: 0,
        }
        for det in detections_list:
            filter_ids[det.fid] += 1
        return filter_ids
    

    def filter_detections(self, fid: int) -> List[ZTFDetection]:
        return [d for d in self.detections if d.fid == fid and not d.dubious and d.rb > 0.3]
    
    def detections_grouped_by_day(self, fid: int) -> Dict[int, ZTFDetection]:
        dets = self.detections_by_fid(fid)
        groups = {}
        for d in dets:
            day = int(d.mjd)
            if day not in groups:
                groups[day] = []
            groups[day].append(d)
        return groups
    
