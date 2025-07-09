from fastapi import APIRouter, UploadFile, File
from app.services.api.template_service import TemplateService
from app.services.api.gemini_redactor_service import GeminiRedactorService

router = APIRouter(prefix="/template", tags=["template"])

# Cargar las secciones de la plantilla para el contexto.
@router.get("/sectionList")
def change_template():
    #return GeminiRedactorUseCase.listar_secciones(template)
    return GeminiRedactorService.listar_secciones()

@router.get("/articleList")
def article_list():
    #return GeminiRedactorUseCase.listar_articulos()
    return {"message": "Listando artículos..."}

@router.get("/articleList/{section}")
def article_list_template(section: str):
    #return GeminiRedactorUseCase.listar_articulos_seccion(section)
    return {"message": f"Listando artículos de la sección {section}..."}

@router.post("/uploadTemplate")
def upload_template(file: UploadFile = File(...)):
    return TemplateService.upload_template(file)