from fastapi import APIRouter
from app.domain.uses_cases.gemini_redactor_use_case import GeminiRedactorUseCase

router = APIRouter(prefix="/template", tags=["gemini"])

# Cargar las secciones de la plantilla para el contexto.
@router.post("/cargarSecciones")
def charge_template():
    return GeminiRedactorUseCase.generate_redaction()

@router.get("/get")
def saludo():
    return {"mensaje": "Este es el objeto de contratacion"}

@router.get("/organizacionContratante")
def hora_actual():
    return {"mensaje": "esta es la organizacion contratante"}
