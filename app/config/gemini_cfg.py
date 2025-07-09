import os
from google.generativeai import genai
import time

class FileGemini:
    def __init__(self, file_path, name):
        self.file_path = file_path
        self.name = name

class GeminiConfig:
    """
    Configuration class for Gemini API.
    """
    def __init__(self):
        self

    def get_model(self):
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
        return model
    
    def upload_file(self, file_path):
        """
        Uploads a file to Gemini's Files API.
        """
        # Sube el archivo
        print(f"Subiendo archivo: {file_path}...")
        uploaded_file = genai.upload_file(
            path=file_path,
            display_name=os.path.basename(file_path),
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

        fileGemini = FileGemini(uploaded_file.uri, uploaded_file.name)

        return fileGemini

