import os
from typing import Optional
from pydantic import BaseModel
from models.tns_object import TNSObject
from models.lasair_object import LasairObject
from models.ztf_object import ZTFObject
from api.alerce_client import AlerceClient
from api.mongo_client import LSSTMongoClient
from api.lasair_client import LasairClient
from plotting import object_viewer
import dotenv

dotenv.load_dotenv()

class SNObject(BaseModel):
    tns_object: TNSObject
    ztf_object: Optional[ZTFObject] = None
    lasair_object: Optional[LasairObject] = None

M = LSSTMongoClient(uri="mongodb://localhost:27017", db_name="lsst-sn-type-analysis")
tns_objects = M.get_all("tns_sn_objects")
tns_objects = [TNSObject(**obj) for obj in tns_objects]
tns_by_name = {obj.name: obj for obj in tns_objects}

ztf_objects = M.get_all("ztf_objects")
ztf_objects = [ZTFObject(**obj) for obj in ztf_objects]
ztf_by_name = {obj.oid: obj for obj in ztf_objects}

lasair_objects = M.get_all("lasair_sn_objects")
lasair_objects = [LasairObject(**obj) for obj in lasair_objects]
lasair_by_tns_name = {obj.tns_name: obj for obj in lasair_objects if obj.tns_name is not None}

sn_objects = []
for name, tns in tns_by_name.items():
    ztf = None
    for internal_name in tns.internal_names:
        ztf = ztf_by_name.get(internal_name)
        if ztf is not None:
            break
    lasair = lasair_by_tns_name.get(name)
    sn_obj = SNObject(tns_object=tns, ztf_object=ztf, lasair_object=lasair)
    sn_objects.append(sn_obj)
       
sn_type_counts = {}
for sn_obj in sn_objects:
    sn_type = sn_obj.tns_object.type
    if sn_type not in sn_type_counts:
        sn_type_counts[sn_type] = [0, 0, 0, 0]

    counts = sn_type_counts[sn_type]
    counts[0] += 1

    if sn_obj.ztf_object is not None:
        counts[1] += 1
    if sn_obj.lasair_object is not None:
        counts[2] += 1
    if sn_obj.ztf_object is None and sn_obj.lasair_object is None:
        counts[3] += 1
    sn_type_counts[sn_type] = counts

for sn_type, count in sorted(sn_type_counts.items(), key=lambda x: x[1][0], reverse=True):
    print(f"|{sn_type}|{count[0]}|{count[1]}|{count[2]}|{count[3]}|")