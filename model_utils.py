# model_utils.py
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Ruta del modelo guardado
MODEL_PATH = "./t5_model"

# Cargar modelo y tokenizer
model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)
tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)

def get_model_and_tokenizer():
    """Devuelve el modelo y el tokenizer ya cargados."""
    return model, tokenizer
