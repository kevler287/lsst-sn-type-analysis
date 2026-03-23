import time
import requests
import os
import dotenv
from api.lasair_client import LasairClient
from api.mongo_client import LSSTMongoClient
from models.dia_object import DiaObject

dotenv.load_dotenv()
token = os.environ.get('LASAIR_API_TOKEN')
L = LasairClient(token=token)
M = LSSTMongoClient(uri="mongodb://localhost:27017", db_name="lsst")

def fetch_all_sn_ids():
    all_ids = []
    offset = 0
    limit = 1000
    while True:
        try:
            batch = L.query(
                selected='sherlock_classifications.diaObjectId',
                tables='sherlock_classifications',
                conditions='classification LIKE "SN"',
                limit=limit,
                offset=offset
            )
            if not batch:
                break
            all_ids.extend([r['diaObjectId'] for r in batch])
            print(f"Fetched {len(all_ids)} IDs so far...")
            if len(batch) < limit:
                break
            offset += limit
        except Exception as e:
            if "API Error 429" in str(e):
                print(f"  → rate limit hit, retrying in 50 minutes...")
                time.sleep(3000)
            else:
                raise
        except requests.exceptions.Timeout:
            print(f"  → timeout, retrying in 5 minutes...")
            time.sleep(300)

    return all_ids

def fetch_object_with_retry(sn_id):
    while True:
        try:
            result = L.get_object(object_id=sn_id, lasair_added=True)
            return result
        except Exception as e:
            if "API Error 429" in str(e):
                print(f"  → rate limit hit, retrying in 50 minutes...")
                time.sleep(3000)
            else:
                raise
        except requests.exceptions.Timeout:
            print(f"  → timeout, retrying in 5 minutes...")
            time.sleep(300)

print("Fetching all SN IDs...")
sn_ids = fetch_all_sn_ids()
total = len(sn_ids)
print(f"Total SN IDs: {total}")

inserted = 0
skipped = 0
failed = 0

for i, sn_id in enumerate(sn_ids):
    print(f"[{i+1}/{total}] Processing {sn_id}...")

    if M.exists(sn_id):
        print(f"  → skipped (already exists)")
        skipped += 1
        continue

    try:
        result = fetch_object_with_retry(sn_id)
        sn_obj = DiaObject.from_dict(result)
        M.insert(sn_obj)
        inserted += 1
        print(f"  → inserted")
    except Exception as e:
        print(f"  → failed: {e}")
        failed += 1

print(f"\nDone. inserted={inserted}, skipped={skipped}, failed={failed}")