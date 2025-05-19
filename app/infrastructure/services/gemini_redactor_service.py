import google.generativeai as genai
from dotenv import load_dotenv
import os
import yaml
import json

#Cargamos las variables de entorno

RESOURCE_PATH = "resources/"

class GeminiRedactorService:

    ## Construimos la isntruccion general. la idea es que cada seccion tenga su propias instrucciones
    def take_instruction(self, instruction):
        """
        Carga el fichero yaml de instrucciones 
        """
        contextfile = os.path.join(RESOURCE_PATH,"contexto_generales.yml")
        try:
            with open(contextfile, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                result = data.get(instruction, [])
                if result:
                    return " ".join(result)
                else:
                    return ""
        except FileNotFoundError:
            print(f"Error: El archivo {contextfile} no se encontró.")
            return None
        

    def take_template(self, template):
        """
        de momento este carga una plantilla pre-construida, la idea es que exista una funcion que genere plantillas
        """

        jsonFile = os.path.join(RESOURCE_PATH,f"template/{template}")
        print(f"JSONFILE: {jsonFile}")
        try:
            with open(jsonFile, 'r', encoding='utf-8') as file:
                return json.load(file)
        
        except FileNotFoundError:
            print(f"Error: El archivo {jsonFile} no se encontró.")
            return None

    ## Servicio para construir el prompt
    def build_prompt(self, instruction, user_context, question):
        """
        construye el prompt con las intrucciones dependiendo de la seccion que le mande
        """
        requerimientos = f"Informacion: {self.take_instruction(instruction)}\n<context>{user_context}<context>\nPregunta:{question}\n"
        print("PROMPT: ",requerimientos)
        return requerimientos



    def generar_texto(self, prompt_usuario ):
        """
        Envía un prompt al modelo Gemini Pro y devuelve la respuesta generada.
        """
        # Asegúrate de tener la biblioteca instalada: pip install google-generativeai
        load_dotenv();
        # Lee la clave de API desde la variable de entorno
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

        # Verifica si la clave de API está configurada
        if not GOOGLE_API_KEY:
            print("Error: La variable de entorno GOOGLE_API_KEY no está configurada.")
            exit()

        # Configura la API de Google Generative AI con tu clave
        genai.configure(api_key=GOOGLE_API_KEY)

        # Selecciona el modelo a usar (Gemini Pro para texto)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        try:
            response = model.generate_content(prompt_usuario)
            return response.text
        except Exception as e:
            return f"Ocurrió un error al interactuar con la API: {e}"