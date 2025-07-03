from app.config.config import db
from models.licitacion_model import Licitacion
from typing import List

collection = db["licitaciones"]


async def insert_licitacion(licitacion: Licitacion):
    result = await collection.insert_one(licitacion.dict())
    return str(result.inserted_id)


async def get_all_licitaciones() -> List[Licitacion]:
    cursor = collection.find({})
    return [Licitacion(**doc) async for doc in cursor]
