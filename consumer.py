import os
import requests
from models.sn_object import SuperNovaDiaObject
from api.lasair_client import LasairClient
from api.mongo_client import SuperNovaMongoClient
import dotenv

dotenv.load_dotenv()

token = os.environ.get('LASAIR_API_TOKEN')
L = LasairClient(token=token)
M = SuperNovaMongoClient(uri="mongodb://localhost:27017", db_name="lsst")

sn_ids = L.query(selected='sherlock_classifications.diaObjectId', tables='sherlock_classifications', conditions='classification LIKE "SN"')
for sn_id in sn_ids:
    sn_id = sn_id['diaObjectId']
    if M.exists(sn_id):
        print(f"Object {sn_id} already exists in the database.")
        continue

    try:
        result = L.get_object(object_id=sn_id, lasair_added=False)
        sn_obj = SuperNovaDiaObject.from_dict(result)
        print(f"Inserting object {sn_id} into the database.")
        M.insert(sn_obj)
    except requests.exceptions.Timeout:
        break

