import os
import dotenv
import pandas as pd
from tqdm import tqdm
from api.mongo_client import LSSTMongoClient
from typing import List
from models.data_models.tns_object import TNSObject, NamePrefix

mongo_client = LSSTMongoClient()
dotenv.load_dotenv()

def fetch_sne_from_tns():
    filepath = "files/tns_public_objects.csv" #TODO: automatic fetching from TNS with TNS bot
    collection   = "tns_sn_objects"

    df = pd.read_csv(filepath, skiprows=1, low_memory=False)
    df = df.drop(columns=["reporters"])
    df = df[df["name_prefix"] == NamePrefix.SN]  # only SNe
    df = df.where(df.notna(), other=None)

    objects: List[TNSObject] = []
    for _, row in df.iterrows():
        try:
            objects.append(TNSObject.model_validate(row.to_dict()))
        except Exception as e:
            print(f"Skipping {row.get('name', '?')}: {e}")

    skipped = 0
    failed = 0
    for obj in tqdm(objects, desc="Fetching TNS objects"):
        if mongo_client.exists(collection, obj.objid):
            skipped += 1
            continue
        try:
            mongo_client.insert(collection, obj)
        except Exception as e:
            print(f"Failed to insert {obj.name}: {e}")
            failed += 1

    print(f"Done. Inserted {len(objects) - skipped - failed}, skipped {skipped}, failed {failed}.")

def fetch_sne_from_lasair():
    from api.lasair_client import LasairClient
    from models.data_models.lasair_object import LasairObject

    L = LasairClient(token=os.getenv("LASAIR_API_TOKEN"))
    LIMIT = 10000
    offset = 0
    collection = "lasair_sn_objects"
    while True:
        objects = L.query(
            selected="*",
            tables="objects, sherlock_classifications",
            conditions="sherlock_classifications.classification='SN'",
            limit=LIMIT,
            offset=offset
        )
        if not objects:
            break

        failed = 0
        skipped = 0
        for obj in tqdm(objects, desc="Fetching Lasair objects"):
            if mongo_client.exists(collection, obj.get("diaObjectId")):
                skipped += 1
                continue
            try:
                lasair_obj = LasairObject(**obj)
                mongo_client.insert(collection, lasair_obj)
            except Exception as e:
                print(f"Failed to insert {obj.get('diaObjectId', '?')}: {e}")
                failed += 1
        
        print(f"Inserted {len(objects) - skipped - failed}, skipped {skipped}, failed {failed}.")
        offset += LIMIT

def fetch_tns_crossmatches_from_alerce():
    from api.alerce_client import AlerceClient
    from models.data_models.ztf_object import ZTFObject, ZTFDetection, ZTFNonDetection, ZTFForcedPhotometry

    tns_objects = mongo_client.get_all("tns_sn_objects")
    tns_objects = [TNSObject(**obj) for obj in tns_objects]

    ztf_matches = []
    for obj in tns_objects:
        if obj.internal_names is None or len(obj.internal_names) == 0:
            continue
        for name in obj.internal_names:
            if "ZTF" in name and name not in ztf_matches:
                ztf_matches.append(name)

    print(f"Found {len(ztf_matches)} ZTF crossmatches.")

    A = AlerceClient()
    not_found = 0
    skipped = 0
    failed = 0
    for ztf_id in tqdm(ztf_matches, desc="Fetching ZTF objects"):
        if mongo_client.exists("ztf_objects", ztf_id):
            skipped += 1
            continue
        try:
            obj = A.py_client.query_object(oid=ztf_id, survey="ztf", format="json")
        except:
            not_found += 1
            continue

        try:
            ztf_obj = ZTFObject(**obj)
            lightcurves = A.py_client.query_lightcurve(oid=ztf_id, survey="ztf", format="json")
            ztf_obj.detections = [ZTFDetection(**det) for det in lightcurves.get("detections", [])]
            ztf_obj.non_detections = [ZTFNonDetection(**nd) for nd in lightcurves.get("non_detections", [])]
            
            forced_photometry = A.py_client.query_forced_photometry(oid=ztf_id, survey="ztf", format="json")
            ztf_obj.forced_photometry = [ZTFForcedPhotometry(**fp) for fp in forced_photometry]
            mongo_client.insert("ztf_objects", ztf_obj)
        except Exception as e:
            print(f"Failed to insert {ztf_id}: {e}")
            failed += 1

    print(f"Done. Inserted {len(ztf_matches) - skipped - failed - not_found}, skipped {skipped}, failed {failed}, not found {not_found}.")

if __name__ == "__main__":
    # fetch_sne_from_tns()
    # fetch_sne_from_lasair()
    fetch_tns_crossmatches_from_alerce()
    mongo_client.close()

