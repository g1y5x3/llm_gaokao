import csv
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "01-ai/Yi-1.5-9B-Chat"
tokenizer = AutoTokenizer.from_pretrained("01-ai/Yi-1.5-9B-Chat", use_fast=False)
model = AutoModelForCausalLM.from_pretrained("01-ai/Yi-1.5-9B-Chat", device_map="auto", torch_dtype='auto').eval()

messages = [
    {"role": "system", "content": "你要回答数学题，题目中涉及到数学公式会以latex代码来表达，你在回答时如果要用到数学公式也要写成latex代码。"},
    {"role": "user",   "content": "双曲线 \Tau: x^2 - \frac{y^2}{b^2} = 1，(b>0)，A_1，A_2 为左右定点，过点 M(-2,0) 的直线 l 交双曲线 T 于两点 P、Q，且点 P 在第一象限，（1）若 e=2 时，求b？（2）若 b=\frac{2\sqrt{6}}{3}，\triangle MA_2P 为等腰三角形时，求 P 的坐标？ （3）过点 Q 作 OQ 延长线交 \Tau 于点 R，若 \vec{A_1R} \cdot \vec{A_2P} = 1，求 b 取值范围？"},
]

input_ids = tokenizer.apply_chat_template(conversation=messages, tokenize=True, return_tensors='pt')
output_ids = model.generate(input_ids.to('cuda'), eos_token_id=tokenizer.eos_token_id, max_length=4096)
response = tokenizer.decode(output_ids[0][input_ids.shape[1]:], skip_special_tokens=True)

print(response)
