from transformers import T5Tokenizer, T5ForConditionalGeneration

class T5Service:
    def __init__(self, model_name="t5-small"):
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)

    def generate_text(self, task: str, text: str, max_length=50):
        input_text = f"{task}: {text}"
        input_ids = self.tokenizer(input_text, return_tensors="pt").input_ids
        output_ids = self.model.generate(input_ids, max_length=max_length)
        return self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
