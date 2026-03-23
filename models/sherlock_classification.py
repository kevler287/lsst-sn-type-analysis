from pydantic import BaseModel, Field
from typing import Optional

class SherlockClassification(BaseModel):

    # Sherlock's classification of the transient and its reliability.
    # classificationReliability: 1 = confident, 2 = possible association
    classification: Optional[str] = Field(None, description="Sherlock's classification of the transient, e.g. 'SN', 'AGN', 'VS'.")
    classificationReliability: Optional[int] = Field(None, description="Reliability of the classification. 1 = confident, 2 = possible association.")

    # Host galaxy properties — critical for both classification and future galaxy analysis.
    # catalogue_object_id is the NED/SDSS identifier and can be used to query additional
    # galaxy properties, or to group all supernovae occurring in the same host galaxy.
    catalogue_object_id: Optional[str] = Field(None, description="Host galaxy identifier in the source catalogue (e.g. NED). Use this to link multiple SNe to the same host or to fetch additional galaxy data.")
    catalogue_object_type: Optional[str] = Field(None, description="Type of the associated catalogue object, e.g. 'galaxy', 'agn'.")
    catalogue_table_name: Optional[str] = Field(None, description="Source catalogue the host galaxy was found in (e.g. 'NED', 'SDSS'). Relevant when fetching additional galaxy data from external APIs.")
    Mag: Optional[float] = Field(None, description="Apparent magnitude of the host galaxy.")

    # Redshift — the most critical field in this model. Without z, absolute magnitudes
    # cannot be computed and SN type discrimination becomes significantly harder.
    z: Optional[float] = Field(None, description="Spectroscopic redshift of the host galaxy. Used to compute luminosity distance and convert apparent to absolute magnitude.")

    # Physical separation between the transient and the host galaxy centre.
    # Type II SNe tend to occur closer to star-forming regions in spiral arms,
    # while Type Ia can occur at larger separations due to the older white dwarf progenitor.
    physical_separation_kpc: Optional[float] = Field(None, description="Physical projected separation between the transient and the host galaxy centre in kiloparsecs.")