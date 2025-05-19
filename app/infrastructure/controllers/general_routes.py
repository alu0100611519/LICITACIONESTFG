from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def raiz():
    return {"mensaje": "API activa"}

@router.get("/saludo")
def saludo():
    return {"mensaje": "¡Hola desde general!"}