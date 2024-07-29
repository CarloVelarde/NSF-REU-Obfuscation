from transformers import LlamaForSequenceClassification, LlamaTokenizer
import torch


model_id = "meta-llama/Meta-Llama-3-8B"

model = LlamaForSequenceClassification.from_pretrained(model_id)
tokenizer = LlamaTokenizer.from_pretrained(model_id)

code_string = "console.log('Hello')"

inputs = tokenizer(code_string, return_tensors="pt", max_length=512, truncation=True)
prompt = "Generate embeddings for this code snippet, considering its functionality and output."

input_dict = {**inputs, "prompt": prompt}
outputs = model(**input_dict)
embeddings = outputs.last_hidden_state[:, 0, :]

print(embeddings)