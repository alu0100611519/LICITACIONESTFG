import google.generativeai as genai
import base64
from dotenv import load_dotenv
import os
import yaml
import json
import time

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
           
    def encode_pdf_to_base64(self,pdf_path):
        with open(pdf_path, "rb") as pdf_file:
            return base64.b64encode(pdf_file.read()).decode("utf-8")
    
    def ask_template(self, request):
        """
        Esta funcion es un ejemplo de como se puede usar la plantilla para generar un texto
        """
        # suponemos que tenemos una carga de plantilla ( realizar en otro servicio).
        pdf_path = os.path.join(os.path.join("resources/template/suministro_abierto.pdf"))
        #pdf_base64 = self.encode_pdf_to_base64(pdf_path)
        #print("PDF Base64:", pdf_base64[:50], "...")

        # Selecciona el modelo a usar (Gemini Pro para texto)
        model = genai.GenerativeModel('gemini-2.0-flash')

        # Sube el archivo
        print(f"Subiendo archivo: {pdf_path}...")
        uploaded_file = genai.upload_file(
            path=pdf_path,
            display_name="Mi Documento PDF para Gemini Flash",
            mime_type="application/pdf"
        )

        print(f"Archivo subido. ID: {uploaded_file.name}")
        print(f"URI del archivo: {uploaded_file.uri}")

        # Opcional pero recomendado: espera a que el archivo esté procesado (READY)
        # Es una buena práctica asegurarse de que el archivo esté listo antes de usarlo
        while uploaded_file.state.name == 'PROCESSING':
            print('Procesando archivo... Esperando 10 segundos.')
            time.sleep(10)
            uploaded_file = genai.get_file(uploaded_file.name) # Actualiza el estado
        if uploaded_file.state.name == 'FAILED':
            raise Exception(f'Error al procesar el archivo: {uploaded_file.name}')
        else:
            print('Archivo listo para usar.')

        # Guarda la URI para el siguiente paso
        file_uri_to_use = uploaded_file.uri


        # Prepara el contenido de la solicitud
        # El tipo MIME para PDF es 'application/pdf'
        contents = [
            {
                "parts": [
                    {"file_data": {"mime_type": "application/pdf", "uri": file_uri_to_use}},
                    {"text": request}
                ]
            }
        ]

        # Genera la respuesta
        response = model.generate_content(contents)

        #print(response.text)

        # Opcional: Si quieres borrar el archivo de la Files API después de usarlo
        genai.delete_file(uploaded_file.name) # Usa uploaded_file.name, no uploaded_file.id
        print(f"Archivo {uploaded_file.name} eliminado de la Files API.")

        return response.text
            
            



