from transformers import T5Tokenizer, T5ForConditionalGeneration

# Cargar modelo y tokenizador
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Texto de entrada (ejemplo de resumen)
input_text = "summarize: OpenAI ha desarrollado ChatGPT, un modelo avanzado de lenguaje basado en IA."
input_ids = tokenizer(input_text, return_tensors="pt").input_ids

# Generar salida
output_ids = model.generate(input_ids, max_length=50)
output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print("Salida:", output_text)
