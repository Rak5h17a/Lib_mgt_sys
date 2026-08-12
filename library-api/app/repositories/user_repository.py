from typing import Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

class UserRepository:

    COLLECTION_NAME = "users"

    def __init__(self, db : AsyncIOMotorDatabase) -> None:
        self._collection= db[self.COLLECTION_NAME]

    async def create(self, data: dict[str,Any]) -> str:
        result = await self._collection.insert_one(data)
        return str(result.inserted_id)

    async def get_by_username(self, username: str) -> dict[str, Any] |None:
        document = await self._collection.find_one({"username": username})
        if document is None:
            return None
        document["id"] = str(document.pop("_id"))
        return document

    async def get_by_id(self, record_id: str) -> dict[str, Any] |None:
        if not ObjectId.is_valid(record_id):
            return None
        document =  await self._collection.find_one({"_id":ObjectId(record_id)})
        if document is None:
            return None
        document["id"] = str(document.pop("_id"))
        return document