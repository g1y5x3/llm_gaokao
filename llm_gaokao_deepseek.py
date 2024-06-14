import csv, torch, argparse
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

parser = argparse.ArgumentParser(description="Run a model on a CSV file and save the responses.")
parser.add_argument("--model_name", default="deepseek-ai/deepseek-math-7b-instruct", type=str, required=False, help="Name of the model to use.")
parser.add_argument("--max_length", default=4096, type=int, required=False, help="Maximum length for the generated response.")
args = parser.parse_args()

model_name = args.model_name
max_length = args.max_length

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.bfloat16).eval()
model.generation_config = GenerationConfig.from_pretrained(model_name)
model.generation_config.pad_token_id = model.generation_config.eos_token_id

with open("data/2024_math_shanghai/exam_with_answer.csv", "r") as input_file:
    csv_reader = csv.reader(input_file)
    next(csv_reader)

    with open(f"response/{model_name.split('/')[1]}-2024_math_shanghai.md", "w") as output_file:
        for i, row in enumerate(csv_reader):
            prompt = row[0]
            answer = row[1]

            messages = [
                {"role": "user",   "content": prompt + "\n请通过逐步推理来解答问题，并把最终答案放置于 \\boxed{}中。"}
            ]

            input_ids = tokenizer.apply_chat_template(conversation=messages, add_generation_prompt=True, return_tensors='pt')
            output_ids = model.generate(input_ids.to('cuda'), max_length=max_length)
            response = tokenizer.decode(output_ids[0][input_ids.shape[1]:], skip_special_tokens=True)

            print(f"#### {i+1}")
            print(f"Prompt: {prompt}\n")
            print(f"Response:\n{response}\n")
            print(f"Answer: {answer}\n")

            output_file.write(f"#### {i+1}\n")
            output_file.write(f"Prompt: {prompt}\n\n")
            output_file.write(f"Response:\n\n{response}\n\n")
            output_file.write(f"Answer:{answer}\n\n")
