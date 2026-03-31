from pymongo import MongoClient
from pydantic import BaseModel
from models.data_models.tns_object import TNSObject
from models.data_models.lasair_object import LasairObject
from models.data_models.ztf_object import ZTFObject

class LSSTMongoClient:
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "lsst-sn-type-analysis"):
        self.client = MongoClient(uri)
        self.database = self.client[db_name]

    def insert(self, collection: str, doc: BaseModel) -> None:
        json = doc.model_dump(by_alias=True, exclude_none=True)
        self.database[collection].insert_one(json)

    def exists(self, collection: str, id: int) -> bool:
        return self.database[collection].count_documents({"_id": id}) > 0
    
    def get_object(self, collection: str, id: int) -> dict:
        return self.database[collection].find_one({"_id": id})
    
    def get_all(self, collection: str) -> list:
        return list(self.database[collection].find())
    
    def count_by(self, collection: str, field: str) -> dict:
        pipeline = [
            {"$sortByCount": f"${field}"}
        ]
        result = self.database[collection].aggregate(pipeline)
        return {doc["_id"]: doc["count"] for doc in result}
    
    def get_tns_ztf_crossmatches(self):
        pipeline = [
            {
                "$lookup": {
                    "from": "ztf_objects",
                    "localField": "internal_names",
                    "foreignField": "_id",
                    "as": "crossmatches"
                }
            },
            {
                "$match": {
                    "crossmatches.0": {"$exists": True}
                }
            },
            {
                "$unwind": "$crossmatches"
            },
            {
                "$replaceRoot": {
                    "newRoot": {
                        "tns": "$$ROOT",
                        "ztf": "$crossmatches"
                    }
                }
            },
            {
                "$unset": "tns.crossmatches"
            }
        ]
        results = self.database["tns_sn_objects"].aggregate(pipeline)

        match_objects = []
        for obj_tuple in results:
            tns_json = obj_tuple["tns"]
            ztf_json = obj_tuple["ztf"]
            match_objects.append((TNSObject(**tns_json), ZTFObject(**ztf_json)))

        return match_objects

    def close(self):
        self.client.close()