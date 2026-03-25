from api.mongo_client import LSSTMongoClient
from plotting import object_viewer

M = LSSTMongoClient(uri="mongodb://localhost:27017", db_name="lsst-sn-type-analysis")
counts = M.count_by("tns_sn_objects", "type")

for sn_type, count in counts.items():
    print(f"{sn_type or 'unclassified':<20} {count}")

