from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# Organizacion contratante
class OrganizacionContratante(BaseModel):
    nombre_contratante: str = Field(alias="nombreContratante")
    telefono: str
    email: str
    id_plataforma: str = Field(alias="id_plataforma")

# Modelo para un lote individual
class Lote(BaseModel):
    numero: str
    name: Optional[str] = Field(None, alias="Name")
    monto_total: Optional[str] = Field(None, alias="montoTotal")
    impuestos_excluidos: Optional[str] = Field(None, alias="impuestosExcluidos")
    cpv_list: Optional[List[str]] = Field(None, alias="cpvList")

# Modelo principal para la Licitacion
class Licitacion(BaseModel):
    title: str
    updated: datetime
    contract_folder_id: str = Field(alias="contract_folder_id")
    organizacion_contratante: OrganizacionContratante
    tipo: str
    sub_tipo: str = Field(alias="subTipo")
    cpv_list: List[str] = Field(alias="cpvList")
    monto_estimado: str = Field(alias="montoEstimado")
    monto_total: str = Field(alias="montoTotal")
    impuestos_excluidos: str = Field(alias="impuestosExcluidos")
    lotes: Optional[List[Lote]] = Field(None, alias="Lotes")
    programa_financiacion: Optional[str] = Field(None, alias="programaFinanciacion")
    legal_document: Optional[str] = Field(None, alias="legalDocument")
    legal_document_uri: Optional[str] = Field(None, alias="legalDocumentURI")