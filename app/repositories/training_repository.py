from transformers import TrainingArguments, Trainer

from datasets import load_dataset

# Cargar dataset desde un archivo JSON
dataset = load_dataset("json", data_files="datos_pliegos.json")

# Ver la estructura de los datos
print(dataset["train"][0])


def preprocess_data(example):
    input_text = "task: " + example["input"]
    target_text = example["output"]

    # Tokenización
    inputs = tokenizer(input_text, padding="max_length", truncation=True, max_length=512)
    targets = tokenizer(target_text, padding="max_length", truncation=True, max_length=512)

    inputs["labels"] = targets["input_ids"]
    return inputs

# Aplicar tokenización al dataset
tokenized_dataset = dataset.map(preprocess_data)

# Definir los argumentos de entrenamiento
training_args = TrainingArguments(
    output_dir="./t5-finetuned",
    per_device_train_batch_size=2,  # Ajustar según la GPU disponible
    num_train_epochs=3,
    logging_dir="./logs",
    save_strategy="epoch",
)

# Crear el Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
)

# Iniciar el fine-tuning
trainer.train()
