from fastapi import APIRouter

router = APIRouter(prefix="/context", tags=["contexto"])

@router.get("/")
def read_root():
    return 

@router.get("/objetoContratacion")
def saludo():
    return {"mensaje": "Este es el objeto de contratacion"}

@router.get("/organizacionContratante")
def hora_actual():
    return {"mensaje": "esta es la organizacion contratante"}