from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "01-ai/Yi-1.5-9B-Chat"
tokenizer = AutoTokenizer.from_pretrained("01-ai/Yi-1.5-9B-Chat", use_fast=False)
model = AutoModelForCausalLM.from_pretrained("01-ai/Yi-1.5-9B-Chat", device_map="auto", torch_dtype='auto').eval()

messages = [
    {"role": "system", "content": "你要回答数学题，题目中涉及到数学公式会以latex代码来表达，你在回答时如果要用到数学公式也要写成latex代码。"},
    {"role": "user",   "content": "已知 k \in R，\vec{a}=(2,5)，\vec{b}=(6,k)，\vec{a}//\vec{b}，则 k 的值为？"},
]

input_ids = tokenizer.apply_chat_template(conversation=messages, tokenize=True, return_tensors='pt')
output_ids = model.generate(input_ids.to('cuda'), eos_token_id=tokenizer.eos_token_id, max_length=4096)
response = tokenizer.decode(output_ids[0][input_ids.shape[1]:], skip_special_tokens=True)

print(response)