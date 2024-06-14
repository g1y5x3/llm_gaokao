import csv
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "01-ai/Yi-1.5-9B-Chat"
tokenizer = AutoTokenizer.from_pretrained("01-ai/Yi-1.5-9B-Chat", use_fast=False)
model = AutoModelForCausalLM.from_pretrained("01-ai/Yi-1.5-9B-Chat", device_map="auto", torch_dtype='auto').eval()

messages = [
    {"role": "user",   "content": "已知 $f(x) = \begin{cases}\sqrt{x}, x > 0 \\1, x \leq 0\end{cases}$，$f(3)=$"},
]

input_ids = tokenizer.apply_chat_template(conversation=messages, tokenize=True, return_tensors='pt')
output_ids = model.generate(input_ids.to('cuda'), eos_token_id=tokenizer.eos_token_id, max_length=4096)
response = tokenizer.decode(output_ids[0][input_ids.shape[1]:], skip_special_tokens=True)

print(response)
