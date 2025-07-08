from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict
from app.domain.uses_cases.api.gemini_redactor_use_case import GeminiRedactorUseCase

router = APIRouter( tags=["gemini"])

# Define la estructura del JSON de entrada
class Pregunta(BaseModel):
    contexto: str
    pregunta: str
    secciones: str = None 

class ListarCPV(BaseModel):
    tipo: str
    subTipo: str
    titulo: str

gemini_redactor_use_case = GeminiRedactorUseCase()
@router.get("/ask")
def ask(peticion: Pregunta) -> Dict[str, str]:
    contexto = peticion.contexto
    pregunta = peticion.pregunta
    
    return {"respuesta": gemini_redactor_use_case.ask_for_template(contexto, pregunta)}

@router.get("/suggestCPVList")
def listar_secciones(listarCPV: ListarCPV):
    """Devuelve una lista de secciones disponibles en la plantilla.
    """
    tipoContrato = listarCPV.tipo
    subTipoContrato = listarCPV.subTipo
    titulo = listarCPV.titulo
    return gemini_redactor_use_case.recomendar_lista_cpv(tipoContrato, subTipoContrato, titulo)

@router.get("/askforSection")
def ask_for_section(peticion: Pregunta) -> Dict[str, str]:
    """Devuelve una respuesta a una pregunta sobre una sección específica de la plantilla.
    """
    contexto = peticion.contexto
    pregunta = peticion.pregunta
    secciones = peticion.secciones
    
    return gemini_redactor_use_case.ask_for_section(contexto, pregunta, secciones)






