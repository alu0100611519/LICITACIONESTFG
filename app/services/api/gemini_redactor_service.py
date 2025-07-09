import google.generativeai as genai

import os
import yaml
from app.config.gemini_cfg import GeminiConfig

#Cargamos las variables de entorno



class GeminiRedactorService:
    def __init__(self):
        """
        Inicializa el servicio de redacción de Gemini.
        """
        # Configura el modelo Gemini.
        self.model = GeminiConfig.get_model()
    
    def build_prompt(self, question, instructions = None, context = None, article= None):
        """
        Construye un prompt basado en una plantilla específica.
        """
        prompt = ""

        # construimos la capa de instrucciones.
        if instructions is None:
            instruction_path = os.path.join(RESOURCE_PATH, "instructions.yml")
            with open(instruction_path, 'r') as file:
                data = yaml.safe_load(file)
                instructions_content = data.get(instructions, [])
                prompt += '\n'.join(f"- {linea}" for linea in instructions_content)

        # construimos el contexto.
        if context is not None:
            prompt += f"<context>{context}</context>\n"

        # construimos la parte de lo  articulos ( sobre todo para la secciones).
        if article is not None:
            prompt += f"<article>{self.take_article(article)}</article>\n"
        
        prompt += f"question: +{question}"
        return prompt
    
    def take_article(self, articles ):
        """
        Toma un artículo específico de la plantilla.
        """
        artcile_path = os.getenv("ARTICLE_PATH", "resources/articles")
        contenido_total = ""
        # Aquí deberías implementar la lógica para obtener el artículo de la plantilla.
        # Por ahora, devolvemos un texto de ejemplo.
        for art in articles:
            ruta_archivo = os.path.join(artcile_path, f"{art}.txt")
            try:
                with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                    contenido = archivo.read()
                    contenido_total += f"{contenido}\n"
                    contenido_total += "<space>\n"
            except FileNotFoundError:
                print(f"Archivo no encontrado: {ruta_archivo}")
            except Exception as e:
                print(f"Error leyendo {ruta_archivo}: {e}")
        return contenido_total

               
    def ask_template(self, context, question):
        """
        Esta funcion es un ejemplo de como se puede usar la plantilla para generar un texto
        """
        prompt_usuario = ""

        # obtenemos el modelo desde el self 
        model = self.model

        # suponemos que tenemos una carga de plantilla ( realizar en otro servicio).
        pdf_path = os.path.join(os.path.join("resources/template/suministro_abierto.pdf"))

        file_to_use = GeminiConfig.upload_file(pdf_path)

        # Prepara el contenido de la solicitud
        # El tipo MIME para PDF es 'application/pdf'
        contents = [
            {
                "parts": [
                    {"file_data": {"mime_type": "application/pdf", "uri": file_to_use.file_path}},
                    {"text": prompt_usuario}
                ]
            }
        ]

        # Genera la respuesta
        response = model.generate_content(contents)

        genai.delete_file(file_to_use.name) # Usa uploaded_file.name, no uploaded_file.id
        print(f"Archivo {file_to_use.name} eliminado de la Files API.")

        return response.text
    
    def listar_secciones(self):
        prompt_usuario = self.build_prompt("listaSecciones", "Lista secciones de la plantilla")
        # obtenemos el modelo desde el self 
        model = self.model
        # suponemos que tenemos una carga de plantilla ( realizar en otro servicio).
        pdf_path = os.path.join(os.path.join("resources/template/suministro_abierto.pdf"))

        file_to_use = GeminiConfig.upload_file(pdf_path)

        contents = [
            {
                "parts": [
                    {"file_data": {"mime_type": "application/pdf", "uri": file_to_use.file_path}},
                    {"text": prompt_usuario}
                ]
            }
        ]

        # Genera la respuesta
        response = model.generate_content(contents)

        genai.delete_file(file_to_use.name) # Usa uploaded_file.name, no uploaded_file.id
        print(f"Archivo {file_to_use.name} eliminado de la Files API.")

        return response.text
            
            



