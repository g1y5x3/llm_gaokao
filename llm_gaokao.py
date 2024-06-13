import csv
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen2-7B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype='auto').eval()

with open("data/2024_math_shanghai/exam_with_answer.csv", "r") as input_file:
    csv_reader = csv.reader(input_file)
    next(csv_reader)

    with open(f"response/{model_name.split('/')[1]}-2024_math_shanghai.txt", "w") as output_file:
        for i, row in enumerate(csv_reader):
            prompt = row[0]
            answer = row[1]

            messages = [
                {"role": "system", "content": "你要回答数学题，题目中涉及到数学公式会以latex代码来表达，你在回答时如果要用到数学公式也要写成latex代码。"},
                {"role": "user",   "content": prompt},
            ]

            input_ids = tokenizer.apply_chat_template(conversation=messages, tokenize=True, return_tensors='pt')
            output_ids = model.generate(input_ids.to('cuda'), eos_token_id=tokenizer.eos_token_id, max_length=4096)
            response = tokenizer.decode(output_ids[0][input_ids.shape[1]:], skip_special_tokens=True)

            print(f"{i+1}. Prompt: {prompt}\n")
            print(f"{i+1}. Response:\n{response}\n")
            print(f"{i+1}. Answer: {answer}\n")

            output_file.write(f"{i+1}. Prompt: {prompt}\n")
            output_file.write(f"{i+1}. Response:\n{response}\n")
            output_file.write(f"{i+1}. Answer:{answer}\n\n")
