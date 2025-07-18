from fastapi import APIRouter, UploadFile, File
from app.services.api.template_service import TemplateService
from app.services.api.gemini_redactor_service import GeminiRedactorService

router = APIRouter(prefix="/template", tags=["template"])

gemini_service = GeminiRedactorService()

# Cargar las secciones de la plantilla para el contexto.
@router.get("/sectionList")
def change_template():
    #return GeminiRedactorUseCase.listar_secciones(template)
    return gemini_service.listar_secciones()

@router.get("/articleList/{section}")
def article_list_template(section: str):
    #return GeminiRedactorUseCase.listar_articulos_seccion(section)
    return gemini_service.listar_articulos_seccion(section)

@router.post("/uploadTemplate")
def upload_template(file: UploadFile = File(...)):
    return TemplateService.upload_template(file)