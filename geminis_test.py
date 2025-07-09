from app.domain.uses_cases.api.gemini_redactor_use_case import GeminiRedactorUseCase
from app.services.api.gemini_redactor_service import GeminiRedactorService
import os
import json
import time

MODEL_TRAINING_PATH = "collection/context.json"

OUTPUTH_TRAINING_PATH = "listar_secciones.txt"


if __name__ == "__main__":
    geminis_redactor_service = GeminiRedactorService()

    if os.path.exists(OUTPUTH_TRAINING_PATH):
        modo = "a"
    else:
        modo = "w"

    with open(MODEL_TRAINING_PATH, "r", encoding="utf-8") as file:
        data_json = json.load(file)
    index = 0 ## idice que usaremos para limitar las preguntas a 15 por minuto.
    for data in data_json:

        if index == 15:
            index = 0
            print("Esperando 60 segundos para evitar el límite de 15 preguntas por minuto...")
            time.sleep(66)
            print("Continuando...")