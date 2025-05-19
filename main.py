import sys
from fastapi import FastAPI
from datetime import datetime
from app.domain.uses_cases.parse_atom_use_case import ParseAtomEntriesUseCase
from app.domain.uses_cases.gemini_redactor_use_case import GeminiRedactorUseCase
import uvicorn

app = FastAPI()

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"mensaje": "API en funcionamiento"}

@app.get("/generartodo")
def saludo():
    return {"mensaje": "¡Hola desde la API en Python!"}

@app.get("/objetivoContratacion")
def hora_actual():
    return {"hora_actual": datetime.now().isoformat()}

# --- Función especial si se ejecuta con "train" ---
def entrenar_modelo():
    use_case = ParseAtomEntriesUseCase()
    use_case.execute()


# --- Punto de entrada del script ---
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "train":
        entrenar_modelo()
    else:
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)



"""import sys
import uvicorn
from fastapi import FastAPI
#from app.infrastructure.controllers import t5_routes

from app.domain.uses_cases.parse_atom_use_case import ParseAtomEntriesUseCase

def train_model():
    use_case = ParseAtomEntriesUseCase()
    parsed_entries = use_case.execute()


if __name__ == "__main__":
        train_model()

"""







"""
from fastapi import FastAPI
from app.infrastructure.controllers import t5_routes

app = FastAPI()

app.include_router(t5_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    print("services finish");
"""
