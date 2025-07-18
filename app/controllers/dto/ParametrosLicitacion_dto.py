from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional


# --- DTO para cada Lote ---
class LoteDTO(BaseModel):
    """
    Representa la información de un lote individual dentro de la licitación.
    """
    numero: str = Field(None, description="Número identificador del lote")
    name: str = Field(None, alias="Name", description="Nombre del lote") 
    montoTotal: float = Field(None, description="Monto total del lote (incluidos impuestos)")
    impuestosExcluidos: float = Field(None, description="Monto del lote (impuestos excluidos)")
    cpvList: List[str] = Field(None, description="Lista de códigos CPV asociados a este lote") 



class ParametrosLicitacionDTO(BaseModel):
    title: str = Field(None, description="Título completo del contrato de la licitación")
    contract_folder_id: str = Field(None, description="ID de la carpeta del contrato")
    nombreContratante: str = Field(None, description="Nombre de la entidad contratante")
    telefono: str = Field(None, description="Número de teléfono de contacto de la entidad contratante")
    email: EmailStr = Field(None, description="Dirección de correo electrónico de contacto de la entidad contratante")
    id_plataforma: str = Field(None, description="ID de la licitación en la plataforma de contratación")
    tipo: str = Field(None, description="Tipo de procedimiento de contratación")
    subTipo: str = Field(None, description="Subtipo de procedimiento de contratación")
    cpvList: List[str] = Field(None, description="Lista de códigos CPV generales de la licitación")
    montoEstimado: float = Field(None, description="Monto estimado del contrato (sin impuestos)")
    montoTotal: float = Field(None, description="Monto total del contrato (incluidos impuestos)")
    impuestosExcluidos: float = Field(None, description="Monto total del contrato (impuestos excluidos)")
    Lotes: List[LoteDTO] = Field(None, description="Lista de lotes que componen la licitación")