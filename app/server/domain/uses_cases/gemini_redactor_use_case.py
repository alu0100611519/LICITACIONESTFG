import os
import json
from app.infrastructure.services.gemini_redactor_service import GeminiRedactorService
from app.infrastructure.services.user_context_service import UserContextService


class GeminiRedactorUseCase:
    def __init__(self):
        self.gemini_redactor_service = GeminiRedactorService()
        self.user_context_service = UserContextService()

    def generate_redaction(self, data_body):
        result = "";
        result += self.generate_contract_objetive(data_body)
        result += self.generate_contract_organization(data_body)
        result += self.generate_legal_regime(data_body)
        return result


    # genera la clausula de Objetivo del contrato
    def generate_contract_objetive(self, data_body):
        result = "" 
        user_context = self.user_context_service.take_context_json("objetoContrato", data_body)
        
        # de momento insinuamos que queremos usara siempr la plantilla, este servicio deberia de cargar la plantilla si esta esta cargada en la parte "frontend"
        json = self.gemini_redactor_service.take_template("suministro_abierto.json")
        result = json.get("disposicion_generales")
        result += json.get("objective_title")


        prompt = self.service.build_prompt("objetoContrato", user_context,"Quiero que me redactes la seccion del objeto del contrato")

        result += self.service.generar_texto(prompt)

        return result
    
    def generate_contract_organization(self, data_body):
        result = ""
        user_context = self.user_context_service.take_context_json("organizacionContratante", data_body)

        json = self.service.take_template("suministro_abierto.json")
        result = json.get("party_title")
        prompt = self.service.build_prompt("OrganoContratacion", user_context,"quiero que redactes el primer parrafo de la organizacion contratante ")
        result += self.service.generar_texto(prompt)
        result += "\n"
        result += json.get("party_22")
        result += json.get("party_23")
        return result
    
    def generate_legal_regime(self, user_context, params_context):
        result = ""
        json = self.service.take_template("suministro_abierto.json")
        result = json.get("legal_regime_title")
        result += json.get("party_31_1")
        if params_context.get("programaFinanciacion") == "EU":
            result += json.get("party_31_UE")

        if float(params_context.get("montoTotal")) >= 100000:
            result += json.get("party_32_over_100")
        else:
            result += json.get("party_32_under_100")        
        return result
    
    def generate_contract_fitness(self, user_context):
        return None
    
    def ask_for_template(self, context, question):
        """
        Genera un texto a partir de una plantilla predefinida
        """
        request = f"<context>{context}<context>\nPregunta: {question}\n"
        return self.gemini_redactor_service.ask_template(request)



