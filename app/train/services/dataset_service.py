import requests
import pdfplumber
import json
import logging

from app.domain.helper.epigrafe_loader import EpigrafeLoader
logging.getLogger("pdfminer").setLevel(logging.ERROR)

log_filename = "log.txt" # fichero que indica si paso algo al obtener el pdf
pdf_filename = "tmp.pdf"
target_filename = "target.json" #json temporal para saber que estoy obteniendo como salida.

class DataSetService:
    """Servicio para procesar el fichero +
    json generado de la fuente de conocimiento para entrenar el modelo"""

    def __init__(self, target_json ,data_json):
        self.data_json = data_json 
        self.target_json = target_json
        self.loader = EpigrafeLoader("resources/codigosCPV.csv")
    
    def append_to_file(self,filename, line):
        with open(filename, 'a') as file:
            file.write(line + '\n')  # Escribir la línea y añadir un salto de línea

    def table_process(self,tables, data):
        data_set_list = []       
        if tables: 
            for i, table in enumerate(tables, start=1):
                if any("OBJETO DEL CONTRATO" in str(cell) for cell in table[0]):  # Recorre la primera fila
                    data_set = {}

                    print(f"🗂️ Tabla {i} contiene 'OBJETO DEL CONTRATO':")
                    # Concatenar todas las filas excepto la primera en un solo string
                    concatenated_text = " ".join(" ".join(map(str, row)) for row in table[1:])
                    #data_set["target_text"] = concatenated_text
                    #print(f"### data_set:{data_set}")
                    data_set_list.append(data_set)
            
        #print(f"Este si: {data_set_list}")
        return data_set_list

    
    def read_legal_pdf(self,data):
        #print(f"$$ esto es el legal document URI: {data["legalDocumentURI"]}\n")
        response = requests.get(data["legalDocumentURI"])
        if response.status_code == 200:
            with open(pdf_filename, "wb") as f:
                f.write(response.content)
            print("✅ PDF descargado correctamente como documento.pdf")
        else:
            self.append_to_file(log_filename, f"Error descargar {data["contract_folder_id"]}, response: {response.status_code} " )  

        if response.status_code == 200:
            #Abrimos el PDF
            data_set_list = []
            with pdfplumber.open(pdf_filename) as pdf:
                for page_num, page in enumerate(pdf.pages[2:], start=1):
                    texto = page.extract_text()
                    print(f"{texto}")
                    print(f"\n📄 Página {page_num}")
                    #data_set_list_example = self.table_process(page.extract_tables(), data)
                    #data_set_list += data_set_list_example
                print(f"DATA: {data_set_list}")
                return data_set_list

    def process_collection_to_context(self):
        """Recorremos todos los valores de la coleccion y los tratamos para añadirlos en el dataset"""

        with open(self.data_json, "r", encoding="utf-8") as file:
            data_list = json.load(file)  # Cargar el JSON en la variable data
            #print(f"$$ data {data_list}\n")
            token_list = [] # la idea  es que esto coja el contexto que existe y le haga un append.
            for data in data_list:
                result ={}
                result["parametros"] = data
                # OBJETO DEL CONTRATO
                title = data.get("title", "")
                cpv_list = data.get("cpvList", [])
                # Lista de CPV
                if cpv_list:
                    cpvListTrain = {}
                    #cpvListTrain["input_text"] = "cpvList: " + ",".join(cpv_list)
                    cpvListTarget = ""
                    #print(f"KEYS: {self.loader.all_codigos()}")
                    for cpv in cpv_list:
                        #print(f"cpv: {cpv}")
                        cpvDescription = self.loader.get_descripcion(cpv)
                        if cpvDescription != "ERROR":
                            cpvListTarget += cpvDescription
                lotes = data.get("Lotes", [])
                loteObjeto =""
                lotePresupuesto = ""
                if lotes != []:
                    loteObjeto = "Lotes:"
                    lotePresupuesto = "Lotes:"
                    for lote in lotes:
                        loteObjeto += f"lote {lote.get("numero")}: -nombre:{lote.get("Name", "")}"
                        lotePresupuesto += f" lote {lote.get("numero")}: -presupuesto: {lote.get("montoTotal", "")} -montoSinImpuestos: {lote.get("impuestosExcluidos", "")}\n"
                        cpvListLot = lote.get("cpvList", [])
                        for cpv in cpvListLot:
                            cpvDescription = self.loader.get_descripcion(cpv)
                            if cpvDescription != "ERROR":
                                loteObjeto += f" -cpvList: {cpvDescription}"
                        loteObjeto += "\n"
                result["objetoContrato"] = f"titulo: {title} + listaCPV: {cpvListTarget} {loteObjeto}"
                result["organizacionContratante"] = f"organizacion: {data.get("nombreContratante", "")}"
                result["presupuestoTotal"] = f"prespuesto: - total: {data.get("montoTotal", "")} - montoSinImpuestos: {data.get("impuestosExcluidos", "")} {lotePresupuesto}"
                #BLOQUE lectura PDF
                #self.read_legal_pdf(data)
                token_list.append(result)
            #print(f"$$ TOKEN: {token_list}")
            if token_list and isinstance(token_list, list):
                with open( self.target_json,"w", encoding="utf-8") as f:
                    json.dump(token_list,f,indent=4, ensure_ascii=False)
        