from pymongo import MongoClient
from typing import Optional
from models.sn_object import SuperNovaDiaObject

class SuperNovaMongoClient:
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "lsst"):
        self.client = MongoClient(uri)
        self.collection = self.client[db_name]["supernova_objects"]

    def insert(self, obj: SuperNovaDiaObject) -> None:
        doc = obj.model_dump()
        self.collection.update_one(
            {"diaObjectId": obj.diaObjectId},
            {"$set": doc},
            upsert=True
        )

    def get(self, dia_object_id: int) -> Optional[SuperNovaDiaObject]:
        doc = self.collection.find_one({"diaObjectId": dia_object_id})
        if doc is None:
            return None
        doc.pop("_id")
        return SuperNovaDiaObject(**doc)
    
    def exists(self, dia_object_id: int) -> bool:
        return self.collection.count_documents({"diaObjectId": dia_object_id}) > 0

    def get_all(self) -> list[SuperNovaDiaObject]:
        docs = self.collection.find()
        return [SuperNovaDiaObject(**{**doc, "_id": None}) for doc in docs]

    def close(self):
        self.client.close()