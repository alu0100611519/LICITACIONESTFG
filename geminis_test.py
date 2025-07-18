from app.services.api.gemini_redactor_service import GeminiRedactorService
from app.controllers.dto.ParametrosLicitacion_dto import ParametrosLicitacionDTO, LoteDTO

import os
import json
import time

MODEL_TRAINING_PATH = "collection/context.json"

OUTPUTH_TRAINING_PATH = "ask_for_section.txt"


if __name__ == "__main__":
    geminis_redactor_service = GeminiRedactorService()

    if os.path.exists(OUTPUTH_TRAINING_PATH):
        modo = "a"
    else:
        modo = "w"

    lote1 = LoteDTO(
        numero= "1",
        name="Vestuario Monocolor (verde, granate, azul y negro)",  
        cpvList=["18100000"],
    )

    lote2 = LoteDTO(
        numero= "2",
        name="Vestuario Visibilidad Realzada (V.R.) (verde)",  
        cpvList=["18100000"],
    )


    params =  ParametrosLicitacionDTO(
        title="Suministro de vestuario y complementos diversos con destino al personal de las distintas Áreas del CIT, incluyendo innovaciones tecnológicas en su fabricación de modo que permita incluir parte del material reciclado en su fabricación/ser reciclados una vez terminada su vida útil, fomentando la economía circular y contratación de personal con dificultades de acceso al mercado laboral",
        contract_folder_id="E2023006355",
        nombreContratante="Consejo de Gobierno Insular del Cabildo Insular de Tenerife",
        telefono="901501901",
        email="test@test.es",
        id_plataforma="E2023006355",
        tipo= "1",
        subTipo= "2",
        cpvList=["18100000"],
        Lotes=[lote1,lote2])

    start_time = time.perf_counter()
    result = geminis_redactor_service.ask_template(params, "OBJETO DEL CONTRATO")
    end_time = time.perf_counter()
    timpo_total = end_time - start_time
    
