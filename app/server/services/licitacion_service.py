from app.domain.models.licitacion_model import Licitacion
from app.domain.repositories.licitatcion_repository import licitacion_repository
from typing import List


async def crear_licitacion(licitacion: Licitacion):
    return await licitacion_repository.insert_licitacion(licitacion)


async def listar_licitaciones() -> List[Licitacion]:
    return await licitacion_repository.get_all_licitaciones()
