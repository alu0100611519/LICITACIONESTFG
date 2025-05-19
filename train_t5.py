from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments, DataCollatorForSeq2Seq
from datasets import load_dataset, DatasetDict
import torch

# Cargar tokenizer y modelo base
tokenizer = T5Tokenizer.from_pretrained("t5-base")
model = T5ForConditionalGeneration.from_pretrained("t5-base")

# Cargar datasets
data_files = {
    "train": "collection/train.json",
    "validation": "collection/eval.json"
}
dataset = load_dataset("json", data_files=data_files)

# Preprocesamiento
def preprocess(example):
    model_inputs = tokenizer(example["input_text"], max_length=512, truncation=True, padding="max_length")
    labels = tokenizer(example["target_text"], max_length=512, truncation=True, padding="max_length")
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_dataset = dataset.map(preprocess, batched=True)

# Configuración del entrenamiento
training_args = TrainingArguments(
    output_dir="./t5_output",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    save_total_limit=2,
)

# Data collator
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

# Entrenador
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# Entrenamiento
trainer.train()

# Guardar el modelo
model.save_pretrained("t5_finetuned_model")
tokenizer.save_pretrained("t5_finetuned_model")
