import csv
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "01-ai/Yi-1.5-9B-Chat"
tokenizer = AutoTokenizer.from_pretrained("01-ai/Yi-1.5-9B-Chat", use_fast=False)
model = AutoModelForCausalLM.from_pretrained("01-ai/Yi-1.5-9B-Chat", device_map="auto", torch_dtype='auto').eval()

messages = [
    {"role": "system", "content": "你要回答数学题，题目中涉及到数学公式会以latex代码来表达，你在回答时如果要用到数学公式也要写成latex代码。"},
    {"role": "user",   "content": "定义集合 M=\{x_0|x_0 \in R, X \in (-\infty, X_0), f(x) < f(x_0)\}，在是的 M=[-1,1] 的所有 f(x) 中，下列成立的是？ A. f(x) 是偶函数 B. f(x) 在 x=2 处取最大值 C. f(x) 严格增 D. f(x) 在 x=-1 处取到极小值"},
]

input_ids = tokenizer.apply_chat_template(conversation=messages, tokenize=True, return_tensors='pt')
output_ids = model.generate(input_ids.to('cuda'), eos_token_id=tokenizer.eos_token_id, max_length=4096)
response = tokenizer.decode(output_ids[0][input_ids.shape[1]:], skip_special_tokens=True)

print(response)
