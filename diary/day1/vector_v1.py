from pydantic import BaseModel, Field
from models.ztf_object import ZTFObject, ZTFDetection
from typing import Optional, Dict, List
import numpy as np

class ZTFVector(BaseModel):

    oid: str = Field(..., alias="_id", description="ZTF object identifier")
    corrected: bool = Field(..., description="Whether photometry has been corrected from host contamination")
    stellar: bool = Field(..., description="Whether the object is classified as stellar and not as transient")

    # g-band
    g_max_magpsf: Optional[float] = Field(None, description="Maximum g-band PSF magnitude")
    g_rise_time: Optional[float] = Field(None, description="Days from first detection to peak")
    g_dm15: Optional[float] = Field(None, description="Magnitude decline 15 days after peak")

    # r-band
    r_max_magpsf: Optional[float] = Field(None, description="Maximum r-band PSF magnitude")
    r_rise_time: Optional[float] = Field(None, description="Days from first detection to peak")
    r_dm15: Optional[float] = Field(None, description="Magnitude decline 15 days after peak")

    # g-r
    g_r_at_peak: Optional[float] = Field(None, description="g-r at time of g-band peak")
    g_r_at_10d: Optional[float] = Field(None, description="g-r at peak+10 days")
    g_r_at_20d: Optional[float] = Field(None, description="g-r at peak+20 days")
    g_r_peak_lag: Optional[float] = Field(None, description="Days between g-band and r-band peaks")

    # target
    sn_type: int = Field(..., description="target class. see enums/sn_type.py")

    @classmethod
    def from_ztf_object(cls, obj: ZTFObject, sn_type: int) -> "ZTFVector":
        g_dets = obj.detections_grouped_by_day(fid=1)
        r_dets = obj.detections_grouped_by_day(fid=2)

        g_peak_mag, g_peak_mjd = cls._get_peak(g_dets)
        r_peak_mag, r_peak_mjd = cls._get_peak(r_dets)

        return cls(**{
            "_id": obj.oid,
            "corrected": obj.corrected,
            "stellar": obj.stellar,

            "g_max_magpsf": g_peak_mag,
            "g_rise_time": cls._get_rise_time(g_dets),
            "g_dm15": cls._get_mag_delta(g_dets, g_peak_mjd+15) if g_peak_mjd else None,

            "r_max_magpsf": r_peak_mag,
            "r_rise_time": cls._get_rise_time(r_dets),
            "r_dm15": cls._get_mag_delta(r_dets, r_peak_mjd+15) if r_peak_mjd else None,

            "g_r_at_peak": cls._get_color(g_dets, r_dets, g_peak_mjd) if g_peak_mjd else None,
            "g_r_at_10d": cls._get_color(g_dets, r_dets, g_peak_mjd + 10) if g_peak_mjd else None,
            "g_r_at_20d": cls._get_color(g_dets, r_dets, g_peak_mjd + 20) if g_peak_mjd else None,
            "g_r_peak_lag": (r_peak_mjd - g_peak_mjd) if (g_peak_mjd and r_peak_mjd) else None,

            "sn_type": sn_type,
        })

    @staticmethod
    def _get_peak(dets: Dict[int, List[ZTFDetection]]):
        if not dets:
            return None, None
        max_mag = np.inf
        peak_day = None
        for day, detections in dets.items():
            avg_mag = np.mean([det.magpsf for det in detections])
            if avg_mag < max_mag:
                max_mag = avg_mag
                peak_day = day
        return max_mag, peak_day
    
    @staticmethod
    def _get_rise_time(dets: Dict[int, List[ZTFDetection]]):
        _, peak_mjd = ZTFVector._get_peak(dets)
        if peak_mjd is None:
            return None
        first_mjd = min(dets.keys())
        return peak_mjd - first_mjd
    
    @staticmethod
    def _get_mag_at(dets: Dict[int, List[ZTFDetection]], target_mjd: Optional[float], window: float = 2.0) -> Optional[float]:
        if not dets or target_mjd is None:
            return None
        avg_mags = []
        for day, detections in dets.items():
            if abs(day - target_mjd) <= window:
                avg_mags.append(np.mean([det.magpsf for det in detections]))
        return np.mean(avg_mags) if avg_mags else None
    
    @staticmethod
    def _get_mag_delta(dets, target_mjd, window=2.0):
        peak_mag, _ = ZTFVector._get_peak(dets)
        mag_at_target = ZTFVector._get_mag_at(dets, target_mjd, window)
        if peak_mag is None or mag_at_target is None:
            return None
        return mag_at_target - peak_mag

    @staticmethod
    def _get_color(g_dets: Dict[int, List[ZTFDetection]], r_dets: Dict[int, List[ZTFDetection]], target_mjd: Optional[float], window: float = 2.0):
        if not g_dets or not r_dets or target_mjd is None:
            return None
        g_mag = ZTFVector._get_mag_at(g_dets, target_mjd, window)
        r_mag = ZTFVector._get_mag_at(r_dets, target_mjd, window)
        if g_mag is not None and r_mag is not None:
            return g_mag - r_mag
        return None
