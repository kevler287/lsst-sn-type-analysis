from pymongo import MongoClient
from typing import Optional
from models.dia_object import DiaObject

class LSSTMongoClient:
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "lsst"):
        self.client = MongoClient(uri)
        self.collection = self.client[db_name]["supernova_objects"]

    def insert(self, obj: DiaObject) -> None:
        doc = obj.model_dump(by_alias=True, exclude_none=True)
        self.collection.insert_one(doc)

    def get(self, dia_object_id: int) -> Optional[DiaObject]:
        doc = self.collection.find_one({"_id": dia_object_id})
        if doc is None:
            return None
        return DiaObject(**doc)
    
    def exists(self, dia_object_id: int) -> bool:
        return self.collection.count_documents({"_id": dia_object_id}) > 0

    def get_all(self) -> list[DiaObject]:
        docs = self.collection.find()
        return [DiaObject(**doc) for doc in docs]

    def close(self):
        self.client.close()