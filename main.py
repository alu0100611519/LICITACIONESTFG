import sys
import uvicorn
from fastapi import FastAPI
from datetime import datetime
from app.controllers import gemini_routes
from app.controllers import template_routes


app = FastAPI()

# --- API Endpoints ---
app.include_router(gemini_routes.router)
app.include_router(template_routes.router)


# --- Punto de entrada del script ---
if __name__ == "__main__":
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
