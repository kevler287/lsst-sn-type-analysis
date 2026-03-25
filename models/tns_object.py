from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import StrEnum
import math

class NamePrefix(StrEnum):
    SN  = "SN"   # Supernova (spectroscopically classified)
    AT  = "AT"   # Astronomical Transient (unclassified)
    FRB = "FRB"  # Fast Radio Burst
    TDE = "TDE"  # Tidal Disruption Event

class TNSObject(BaseModel):
    objid: int = Field(alias="_id", description="Unique internal object ID assigned by the TNS")
    name_prefix: NamePrefix = Field(description="Prefix of the object name")
    name: str = Field(description="IAU designation of the object, e.g. '2026hdb'. Combined with name_prefix forms the full name, e.g. 'SN 2026hdb'")
    ra: float = Field(description="Right Ascension in decimal degrees (J2000)")
    declination: float = Field(description="Declination in decimal degrees (J2000)")
    redshift: Optional[float] = Field(None, description="Spectroscopic redshift (z) of the object, if measured")
    typeid: Optional[int] = Field(None, description="Internal TNS ID of the object type, corresponds to the 'type' field")
    type: Optional[str] = Field(None, description="Classification type of the object, e.g. 'SN Ia', 'SN II', 'SN Ib/c'")
    reporting_groupid: Optional[int] = Field(None, description="Internal TNS ID of the reporting group, corresponds to the 'reporting_group' field")
    reporting_group: Optional[str] = Field(None, description="Name of the group that officially submitted the discovery report, e.g. 'YSE', 'ZTF'")
    source_groupid: Optional[int] = Field(None, description="Internal TNS ID of the source group, corresponds to the 'source_group' field")
    source_group: Optional[str] = Field(None, description="Name of the group whose data served as the source of the discovery, often identical to reporting_group")
    discoverydate: Optional[datetime] = Field(None, description="Date and time of the first detection (UT)")
    discoverymag: Optional[float] = Field(None, description="Brightness (magnitude) of the object at the time of discovery")
    discmagfilter: Optional[float] = Field(None, description="Internal TNS ID of the filter in which the discovery magnitude was measured")
    band_filter: Optional[str] = Field(None, alias="filter", description="Short name of the photometric filter used for the discovery measurement, e.g. 'g', 'r', 'i', 'z'")
    time_received: Optional[datetime] = Field(None, description="Timestamp at which the report was received by the TNS (UT)")
    internal_names: List[str] = Field(default_factory=list, description="Internal survey names of the object, e.g. 'ZTF21abcdefg'. Important for connecting to lsst data")
    discovery_ads_bibcode: Optional[str] = Field(None, alias="Discovery_ADS_bibcode", description="NASA ADS bibcode of the official TNS discovery report")
    class_ads_bibcodes: Optional[str] = Field(None, alias="Class_ADS_bibcodes", description="NASA ADS bibcode(s) of the TNS classification report(s), multiple entries separated by commas")
    creationdate: Optional[datetime] = Field(None, description="Timestamp when the object entry was created in the TNS (UT)")
    lastmodified: Optional[datetime] = Field(None, description="Timestamp of the last modification to the object entry in the TNS (UT)")

    model_config = {"populate_by_name": True}

    @field_validator("*", mode="before")
    @classmethod
    def empty_string_to_none(cls, v):
        try:
            if math.isnan(v):
                return None
        except TypeError:
            pass
        if isinstance(v, str) and v.strip() == "":
            return None
        return v

    @field_validator("internal_names", mode="before")
    @classmethod
    def parse_internal_names(cls, v):
        try:
            if math.isnan(v):
                return []
        except TypeError:
            pass
        if v is None or (isinstance(v, str) and v.strip() == ""):
            return []
        if isinstance(v, str):
            return [name.strip() for name in v.split(",")]
        if isinstance(v, float):  # e.g. 3.138e+17 → hanlde as str
            return [str(int(v))]
        return v