from app.infrastructure.services.gemini_redactor_service import GeminiRedactorService


class GeminiRedactorUseCase:
    def __init__(self):
        self.service = GeminiRedactorService()

    def generate_redaction(self, user_context):
        resutl = "";
        return 


    # genera la clausula de Objetivo del contrato
    def generate_contract_objetive(self):
        result = "" 
        user_context = data.get("objetoContrato")
        json = self.service.take_template("suministro_abierto.json")
        result = json.get("disposicion_generales")
        result += json.get("objective_title")
        prompt = self.service.build_prompt("objetoContrato", user_context,"Quiero que me redactes la seccion del objeto del contrato")

        result += self.service.generar_texto(prompt)

        return result
    
    def generate_contract_organization(self, user_context):
        result = ""
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


