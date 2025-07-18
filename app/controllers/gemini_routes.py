from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict
from app.services.api.gemini_redactor_service import GeminiRedactorService
from app.controllers.dto.ParametrosLicitacion_dto import ParametrosLicitacionDTO
import logging

router = APIRouter( tags=["gemini"])



logger = logging.getLogger("gemini_routes")
logger.setLevel(logging.INFO)

# Define la estructura del JSON de entrada
class Pregunta(BaseModel):
    contexto: str
    pregunta: str
    secciones: str = None 

class ListarCPV(BaseModel):
    tipo: str
    subTipo: str
    titulo: str

gemini_service = GeminiRedactorService()

@router.post("/ask"
            , response_model= str
            , summary="Responder a una pregunta sobre la plantilla",
            responses={
        200: {"description": "Respuesta generada correctamente"},
        400: {"description": "Solicitud malformada o sin datos suficientes"},
    })
def ask(peticion: Pregunta) -> Dict[str, str]:
    contexto = peticion.contexto
    pregunta = peticion.pregunta
    logger.info(f"Pregunta recibida: {pregunta} con contexto: {contexto}")
    return gemini_service.ask(contexto, pregunta)

@router.post("/askForSection"
            , response_model= str
            , summary="Responder a una pregunta sobre la plantilla",
            responses={
        200: {"description": "Respuesta generada correctamente"},
        400: {"description": "Solicitud malformada o sin datos suficientes"},
    })
def ask_for_section(peticion: ParametrosLicitacionDTO, section: str) -> Dict[str, str]:
    return gemini_service.ask_template(peticion, section)

@router.get("/suggestCPVList")
def listar_secciones(titulo):
    """Devuelve una lista de secciones disponibles en la plantilla.
    """
    return gemini_service.recomendar_cpv( titulo)





