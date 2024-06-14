import csv
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen2-7B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype='auto').eval()

with open("data/2024_math_shanghai/exam_with_answer.csv", "r") as input_file:
    csv_reader = csv.reader(input_file)
    next(csv_reader)

    with open(f"response/{model_name.split('/')[1]}-2024_math_shanghai.md", "w") as output_file:
        for i, row in enumerate(csv_reader):
            prompt = row[0]
            answer = row[1]

            messages = [
                {"role": "user",   "content": prompt},
            ]

            # # llama-3
            # input_ids = tokenizer.apply_chat_template(conversation=messages, add_generation_prompt=True, return_tensors='pt')
            # terminators = [tokenizer.eos_token_id, tokenizer.convert_tokens_to_ids("<|eot_id|>")]
            # output_ids = model.generate(input_ids.to('cuda'), eos_token_id=terminators, pad_token_id=tokenizer.eos_token_id,  max_length=4096)
            input_ids = tokenizer.apply_chat_template(conversation=messages, tokenize=True, add_generation_prompt=True, return_tensors='pt')
            output_ids = model.generate(input_ids.to('cuda'), eos_token_id=tokenizer.eos_token_id, max_length=4096)
            response = tokenizer.decode(output_ids[0][input_ids.shape[1]:], skip_special_tokens=True)

            print(f"#### {i+1}")
            print(f"Prompt: {prompt}\n")
            print(f"Response:\n{response}\n")
            print(f"Answer: {answer}\n")

            output_file.write(f"#### {i+1}\n")
            output_file.write(f"Prompt: {prompt}\n\n")
            output_file.write(f"Response:\n\n{response}\n\n")
            output_file.write(f"Answer:{answer}\n\n")
