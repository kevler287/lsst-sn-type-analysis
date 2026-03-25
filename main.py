import os
from models.tns_object import TNSObject
from models.lasair_object import LasairObject
from api.mongo_client import LSSTMongoClient
from api.lasair_client import LasairClient
from plotting import object_viewer
import dotenv

dotenv.load_dotenv()

M = LSSTMongoClient(uri="mongodb://localhost:27017", db_name="lsst-sn-type-analysis")
tns_objects = M.get_all("tns_sn_objects")
tns_objects = [TNSObject(**obj) for obj in tns_objects]
tns_by_name = {obj.name: obj for obj in tns_objects}

lasair_objects = M.get_all("lasair_sn_objects")
lasair_objects = [LasairObject(**obj) for obj in lasair_objects]

crossmatches = []
no_tns_entry = []
types = {}
for lasair_obj in lasair_objects:
    tns_name = lasair_obj.tns_name
    if tns_name is None:
        continue
    if tns_name in tns_by_name:
        crossmatches.append(tns_name)
        if tns_by_name[tns_name].type not in types:
            types[tns_by_name[tns_name].type] = 0
        types[tns_by_name[tns_name].type] += 1
    else:
        no_tns_entry.append(tns_name)

print(len(crossmatches))
print(len(no_tns_entry))
for type, count in types.items():
    print(type, count)
