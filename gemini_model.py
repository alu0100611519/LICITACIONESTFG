import google.generativeai as genai
from dotenv import load_dotenv
import os

# Asegúrate de tener la biblioteca instalada: pip install google-generativeai
load_dotenv();
# Lee la clave de API desde la variable de entorno
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
print(f"GOOGLE_API_KEY: {GOOGLE_API_KEY}")

# Verifica si la clave de API está configurada
if not GOOGLE_API_KEY:
    print("Error: La variable de entorno GOOGLE_API_KEY no está configurada.")
    exit()

# Configura la API de Google Generative AI con tu clave
genai.configure(api_key=GOOGLE_API_KEY)

# Selecciona el modelo a usar (Gemini Pro para texto)
model = genai.GenerativeModel('gemini-2.0-flash')

def interactuar_con_gemini(prompt_usuario):
    """
    Envía un prompt al modelo Gemini Pro y devuelve la respuesta generada.
    """
    try:
        response = model.generate_content(prompt_usuario)
        return response.text
    except Exception as e:
        return f"Ocurrió un error al interactuar con la API: {e}"

if __name__ == "__main__":
    print("¡Bienvenido a la interacción con la API de Gemini Pro!")
    pregunta_usuario = """dado este contexto <context> tipoContrato: Suministro procedimiento: Abierto montoMacroEstimado: 1145059.2 montoMacroTotal: 844974.72 impuestosMacroExcluidos: 789696 duracion: 4 años prorgable: 1 año
-lote 01 Name: Trece 13 vehículos tipo turismo SUV HEV montoTotal: 437330.4 impuestosExcluidos: 408720 
-lote 02 Name: Ocho 8 vehículos mixtos tipo furgón de 5 plazas montoTotal: 290081.28 impuestosExcluidos: 271104 cpvList: 34111200 
-lote 03 Name: Tres 3 vehículos tipo turismo EV 100 por ciento eléctricos montoTotal: 117563.04 impuestosExcluidos: 109872 </context>
generar una seccion de presupuestos
## instrucciones basicas:
- no quiero una conversacion 
- definir este titulo de la seccion como "PRESUPUESTO BASE DE LICITACIÓN, VALOR ESTIMADO, PRESUPUESTO DE LICITACIÓN Y PRECIO DEL ACUERDO MARCO Y DE LOS CONTRATOS BASADOS."
- tener de acuerdo la ley LCSP que sea necesario 
- en la seccion va el articulo 100.3 de la ley LCSP, que dice "no será necesario que se
apruebe un presupuesto base de licitación con carácter previo a la tramitación del acuerdo
marco, por lo que las referencias al mismo en este pliego se entienden referidas a una
estimación del gasto, sin que el Cabildo, Ayuntamientos y los Entes del Sector Público
Insular estén obligados a llevar a efecto una determinada cuantía de suministro,
calculándose el mismo en aras a determinar el procedimiento de licitación", necesito que se añada este parrafo literal al principio de la salida solo una vez.
- generar una tabla con el costo estimado, el impuesto y el presupuesto base de licitacion
- el impuesto es IGIC, en este caso varia de un 0% hasta un 3%"""

    respuesta_gemini = interactuar_con_gemini(pregunta_usuario)
    print("\nRespuesta de Gemini Pro:")
    print(respuesta_gemini)
    print("-" * 100)