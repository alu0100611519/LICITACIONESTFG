from transformers import T5Tokenizer, T5ForConditionalGeneration

# Cargar el modelo entrenado
model_path = "t5_finetuned_model"
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

# Input de prueba
input_text = "cpvList: 35111200,44480000,35111510,42122110"
inputs = tokenizer(input_text, return_tensors="pt", padding=False, truncation=True)

# Generar salida
output_ids = model.generate(inputs["input_ids"], max_length=512, num_beams=4, early_stopping=True)
output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print("\n📝 Resultado generado:\n")
print(output_text)
