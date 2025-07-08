from fastapi import APIRouter
from app.domain.uses_cases.api.gemini_redactor_use_case import GeminiRedactorUseCase

router = APIRouter(prefix="/template", tags=["gemini"])

# Cargar las secciones de la plantilla para el contexto.
@router.post("/listarSecciones")
def charge_template(template: str):
    return GeminiRedactorUseCase.listar_secciones(template)
