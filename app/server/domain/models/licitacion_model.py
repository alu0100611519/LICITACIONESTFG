from typing import List, Optional
from pydantic import BaseModel, Field


class Lote(BaseModel):
    numero: str
    Name: str
    montoTotal: str
    impuestosExcluidos: str
    cpvList: List[str]


class Licitacion(BaseModel):
    origen: str
    title: str
    updated: str
    contract_folder_id: str
    nombreContratante: str
    telefono: str
    email: str
    id_plataforma: str
    tipo: str
    subTipo: str
    cpvList: List[str]
    montoEstimado: str
    montoTotal: str
    impuestosExcluidos: str
    Lotes: List[Lote]
    programaFinanciacion: str
    legalDocument: str
    legalDocumentURI: str
