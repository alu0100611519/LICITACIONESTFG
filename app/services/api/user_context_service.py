from typing import Any
from app.controllers.dto.ParametrosLicitacion_dto import ParametrosLicitacionDTO
from app.utils.helper.epigrafe_loader import EpigrafeLoader

class UserContextService:
    def __init__(self):
        self.epigrafeLoader = EpigrafeLoader("resources/codigosCPV.csv")

    """
    Service to manage user context.
    """
    def build_paramestros_licitacion_context(self, context: ParametrosLicitacionDTO):
        """
        Load the context from a JSON file.
        """
        result = "";

        if context.title is not None:
            result += f"- titulo:{context.title}\n"
        if context.contract_folder_id is not None:
            result += f"- id del contrato: {context.contract_folder_id}\n"
        if context.nombreContratante is not None:
            result += f"- Organismo Contratacion: {context.nombreContratante}\n"
        if context.id_plataforma is not None:
            result += f"- id del Organismo de contratacion: {context.id_plataforma}\n"
        if context.tipo is not None:
            result += f"- Tipo de contrato: {context.tipo}\n"
        if context.cpvList is not None:
            result += self.build_cpv_list(context.cpvList)
        

        return result
    
    def build_cpv_list(self, cpvList):
        print(f"LISTA -> {cpvList}")
        result = "- cpvlist: "

        if  not cpvList:
            return ""
        
        for item in cpvList:
            result += f"{self.epigrafeLoader.get_descripcion(item)},"

        return result;
        
