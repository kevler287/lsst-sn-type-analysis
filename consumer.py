from tqdm import tqdm
from api.alerce_client import AlerceClient
from api.mongo_client import LSSTMongoClient

A = AlerceClient()
M = LSSTMongoClient(uri="mongodb://localhost:27017", db_name="lsst")

sn_objects = A.fetch_sn_object_ids()

for sn_obj in tqdm(sn_objects):
    if M.exists(sn_obj.diaObjectId):
        continue
    dia_sources = A.fetch_detections(sn_obj.diaObjectId)
    if len(dia_sources) < 5:
        continue
    sn_obj.sources = dia_sources
    M.insert(sn_obj)
