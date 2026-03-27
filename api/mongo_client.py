from pymongo import MongoClient
from pydantic import BaseModel

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

    def close(self):
        self.client.close()