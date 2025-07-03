from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict
from app.domain.uses_cases.gemini_redactor_use_case import GeminiRedactorUseCase

router = APIRouter( tags=["gemini"])

# Define la estructura del JSON de entrada
class Pregunta(BaseModel):
    contexto: str
    pregunta: str

gemini_redactor_use_case = GeminiRedactorUseCase()
@router.post("/ask")
def ask(peticion: Pregunta) -> Dict[str, str]:
    contexto = peticion.contexto
    pregunta = peticion.pregunta

    # Lógica de ejemplo (puedes conectar con un modelo de IA aquí)
    respuesta = f"Has preguntado: '{pregunta}' sobre el contexto: '{contexto[:100]}...'"
    
    return {"respuesta": gemini_redactor_use_case.ask_for_template(contexto, pregunta)}

@router.get("/listaSecciones")
def listar_secciones_template(peticion: Pregunta):
    """Devuelve una lista de secciones disponibles en la plantilla.
    """

    return {"mensaje": "Este es el objeto de contratacion"}

@router.get("/organizacionContratante")
def hora_actual():
    return {"mensaje": "esta es la organizacion contratante"}




