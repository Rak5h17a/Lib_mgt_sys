from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase 
from app.repositories.base import BaseRepository

class ItemRepository(BaseRepository):
    COLLECTION_NAME="items"

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._collection=db[self.COLLECTION_NAME]

    @staticmethod
    def _to_dict_(document: dict[str, Any]) -> dict[str, Any]:
        document["id"]=str(document.pop("_id"))
        return document

    @staticmethod
    def _is_valid_id(record_id:str) -> bool:
        return ObjectId.is_valid(record_id)

    async def create(self, data: dict[str, Any])-> str:
        result=await self._collection.insert_one(data)
        return str(result.inserted_id)

    async def get_by_id(self, record_id:str)-> dict[str,Any] | None:
        if not self._is_valid_id(record_id):
            return None
        document= await self._collection.find_one({"_id":ObjectId(record_id)})
        return self._to_dict_(document) if document else None 

    async def get_all(self) -> list[dict[str,Any]]:
        documents=await self._collection.find().to_list(length=None)
        return [self._to_dict_(doc) for doc in documents]

    async def update(self, record_id: str, data: dict[str,Any])-> bool:
        if not self._is_valid_id(record_id):
            return False 
        result=await self._collection.update_one(
            {"_id":ObjectId(record_id)}, {"$set":data})
        return result.modified_count>0

    async def delete(self,record_id:str) -> bool:
        if not self._is_valid_id(record_id):
            return False 
        result= await self._collection.delete_one({"_id":ObjectId(record_id)})
        return result.deleted_count>0