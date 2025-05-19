from app.domain.uses_cases.gemini_redactor_use_case import GeminiRedactorUseCase
import os
import json
import time

MODEL_TRAINING_PATH = "collection/context.json"

OUTPUTH_TRAINING_PATH = "prueba.txt"


if __name__ == "__main__":
    use_case = GeminiRedactorUseCase()
    with open(MODEL_TRAINING_PATH, "r", encoding="utf-8") as file:
        data_json = json.load(file)
    index = 0 ## idice que usaremos para limitar las preguntas a 15 por minuto.
    for data in data_json:
        user_context = data.get("objetoContrato")
        organization_context = data.get("organizacionContratante")
        budget_context = data.get("presupuestoTotal")
        params_context = data.get("parametros")
        if user_context is not None:
            # Aquí puedes usar el user_context como desees
            if os.path.exists(OUTPUTH_TRAINING_PATH):
                modo = "a"
            else:
                modo = "w"
            with open(OUTPUTH_TRAINING_PATH, modo, encoding='utf-8') as archivo:
                archivo.write("#### PRUEBA DE REDACCION (A PARTIR DE PLANTILLA) ####\n")
                archivo.write(use_case.generate_contract_objetive(user_context) )
                archivo.write("--------------------------------------------------------------------------\n")
                archivo.write(use_case.generate_contract_organization(organization_context))
                archivo.write("--------------------------------------------------------------------------\n")
                archivo.write(use_case.generate_legal_regime(user_context, params_context) )
                index += 3
            if index == 15:
                index = 0
                print("Esperando 60 segundos para evitar el límite de 15 preguntas por minuto...")
                time.sleep(66)
                print("Continuando...")
