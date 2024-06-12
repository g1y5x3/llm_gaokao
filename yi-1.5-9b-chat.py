from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "01-ai/Yi-1.5-9B-Chat"

tokenizer = AutoTokenizer.from_pretrained("01-ai/Yi-1.5-9B-Chat", use_fast=False)

model = AutoModelForCausalLM.from_pretrained("01-ai/Yi-1.5-9B-Chat", device_map="auto", torch_dtype='auto').eval()

messages = [
    {"role": "system", "content": "你要回答数学题, 题目中涉及到数学表达式会以latex的方式来体现, 你在回答时如果要用到数学表达式也用latex代码"},
    {"role": "user", "content": "已知抛物线 y^2=4x 上有一点 P 到准线的距离为 9, 那么 P 到 x 轴的距离为?"},
]

input_ids = tokenizer.apply_chat_template(conversation=messages, tokenize=True, return_tensors='pt')
output_ids = model.generate(input_ids.to('cuda'), eos_token_id=tokenizer.eos_token_id, max_length=4096)
response = tokenizer.decode(output_ids[0][input_ids.shape[1]:], skip_special_tokens=True)

print(response)