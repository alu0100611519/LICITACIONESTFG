from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/")
def read_root():
    return {"mensaje": "API en funcionamiento"}

@router.get("/saludo")
def saludo():
    return {"mensaje": "¡Hola desde la API en Python!"}

@router.get("/hora")
def hora_actual():
    return {"hora_actual": datetime.now().isoformat()}