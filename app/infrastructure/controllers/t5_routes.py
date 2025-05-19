from fastapi import APIRouter
from app.infrastructure.services.t5_service import T5Service

router = APIRouter()
t5_service = T5Service()

@router.post("/t5/generate/")
async def generate_t5_text(task: str, text: str):
    result = t5_service.generate_text(task, text)
    return {"output": result}