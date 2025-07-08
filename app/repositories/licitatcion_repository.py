from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from models import Licitacion
from datetime import datetime

class LicitacionRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["licitaciones"]

    async def insert(self, licitacion: Licitacion) -> str:
        doc = licitacion.dict(by_alias=True)
        result = await self.collection.insert_one(doc)
        return str(result.inserted_id)

    async def get_by_id(self, licitacion_id: str) -> Optional[Licitacion]:
        doc = await self.collection.find_one({"_id": ObjectId(licitacion_id)})
        if doc:
            return Licitacion.parse_obj(doc)
        return None

    async def list_all(self) -> List[Licitacion]:
        cursor = self.collection.find()
        results = []
        async for doc in cursor:
            results.append(Licitacion.parse_obj(doc))
        return results

    async def update(self, licitacion_id: str, licitacion: Licitacion) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(licitacion_id)},
            {"$set": licitacion.dict(by_alias=True)}
        )
        return result.modified_count == 1

    async def delete(self, licitacion_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(licitacion_id)})
        return result.deleted_count == 1
