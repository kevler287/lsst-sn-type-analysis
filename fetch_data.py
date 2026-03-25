import os
import dotenv
import pandas as pd
from tqdm import tqdm
from api.mongo_client import LSSTMongoClient
from typing import List
from models.tns_object import TNSObject, NamePrefix

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
    from models.lasair_object import LasairObject

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


if __name__ == "__main__":
    fetch_sne_from_tns()
    fetch_sne_from_lasair()
    mongo_client.close()

