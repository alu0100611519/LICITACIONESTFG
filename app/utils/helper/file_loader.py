import xml.etree.ElementTree as ET
import os 
from dotenv import load_dotenv

class FileLoader:
    """Clase encargada de cargar un fichero XML."""

    @staticmethod
    def load_xml():
        # cargamos variable de entornos
        load_dotenv();

        # Obtener la ruta base desde la variable de entorno
        base_path = os.getenv("DATA_FILE_PATH", "data/atom/")  # Si no está definida, usa "data/"

        # Si es un archivo específico, conviértelo en una lista
        if os.path.isfile(base_path):
            files = [base_path]
        else:
            # Obtener todos los archivos .atom dentro de la carpeta
            files = [os.path.join(base_path, f) for f in os.listdir(base_path) if f.endswith(".atom")]
        
        if not files:
            print("❌ No se encontraron archivos .atom en la carpeta especificada.")
            return []
        
        tree = None
        i = 0
        for file_path in files:
            try:
                tree = ET.parse(file_path)
                parsed_trees.append(tree)
                print(f"✅ Archivo procesado correctamente: {file_path}")
            except Exception as e:
                print(f"⚠️ Error cargando el fichero {file_path}: {e}")
        
        return parsed_trees
