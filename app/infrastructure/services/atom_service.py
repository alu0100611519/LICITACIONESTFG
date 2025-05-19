from app.domain.core.atom_parser import AtomParser
import xml.etree.ElementTree as ET
import os 
from dotenv import load_dotenv
import json

namespaces = {
    'atom': 'http://www.w3.org/2005/Atom'
}

class AtomService:
    """Servicio que procesa múltiples entradas de un fichero Atom."""


    def process_atom_files_to_json(self):
        all_data=[]
        load_dotenv();
        # Obtener la ruta base desde la variable de entorno
        base_path = os.getenv("DATA_FILE_PATH", "data/atom/")  # Si no está definida, usa "data/"
        for dir_name in os.listdir(base_path):
            print(f"ESTO {dir_name}")
            dir_path = os.path.join(base_path, dir_name)
            if not os.path.isdir(dir_path):
                continue  # saltar si no es una carpeta

            all_data = []  # Limpiamos por cada carpeta
            print(f"📁 Procesando carpeta: {dir_name}")

            for fileName in os.listdir(dir_path):
                if fileName.endswith(".atom"):
                    file_path = os.path.join(dir_path, fileName)
                    try:
                        tree = ET.parse(file_path)
                        root = tree.getroot()

                        #Aqui procesamos el atom y montamos el .json
                        data = AtomParser.parse_entry(root)
                        all_data.extend(data)
                        print(f"✅ Procesado: {fileName}")      
                    except Exception as e:
                        print(f" Error en {fileName}: {e}")
            # Guardar el resultado por carpeta
            output_filename = f"output/{dir_name}_parsed.json"            
            self.append_data_to_json(output_filename,all_data)
            print(f"📝 Guardado en: {output_filename}\n")
            


    def append_data_to_json(self,output, data):
        # Abrimos el archivo de salida en modo escritura
        with open(output, "w", encoding="utf-8") as out_file:
            json.dump(data,out_file,ensure_ascii=False, indent=2)

