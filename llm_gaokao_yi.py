import csv, argparse
from transformers import AutoModelForCausalLM, AutoTokenizer

parser = argparse.ArgumentParser(description="Run a model on a CSV file and save the responses.")
parser.add_argument("--model_name", default="01-ai/Yi-1.5-9B-Chat", type=str, required=False, help="Name of the model to use.")
parser.add_argument("--max_length", default=4096, type=int, required=False, help="Maximum length for the generated response.")
parser.add_argument("--exam", default="shanghai", type=str, required=False, help="Name of the exam for the model to take.")
args = parser.parse_args()

model_name = args.model_name
max_length = args.max_length
exam       = args.exam

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto").eval()

# actual test
with open(f"data/2024_math_{exam}/exam_with_answer.csv", "r") as input_file:
    csv_reader = csv.reader(input_file)
    next(csv_reader)

    with open(f"response/{model_name.split('/')[1]}-2024_math_{exam}.md", "w") as output_file:
        for i, row in enumerate(csv_reader):
            prompt = row[0]
            answer = row[1]

            messages = [
                {"role": "user",   "content": prompt + "\n请通过逐步推理来解答问题，并把最终答案放置于 \\boxed{}中。"}
            ]

            input_ids = tokenizer.apply_chat_template(conversation=messages, tokenize=True, return_tensors='pt')
            output_ids = model.generate(input_ids.to('cuda'), eos_token_id=tokenizer.eos_token_id, max_length=max_length)
            response = tokenizer.decode(output_ids[0][input_ids.shape[1]:], skip_special_tokens=True)

            print(f"#### {i+1}")
            print(f"Prompt: {prompt}\n")
            print(f"Response:\n{response}\n")
            print(f"Answer: {answer}\n")

            output_file.write(f"#### {i+1}\n")
            output_file.write(f"Prompt: {prompt}\n\n")
            output_file.write(f"Response:\n\n{response}\n\n")
            output_file.write(f"Answer:{answer}\n\n")


# contamination test
with open(f"data/contamination_test/exam_with_answer.csv", "r") as input_file:
	csv_reader = csv.reader(input_file)
	next(csv_reader)

	with open(f"response/{model_name.split('/')[1]}-contamination-test.md", "w") as output_file:
		for i, row in enumerate(csv_reader):
			# if the answer matches the answers in the CSV, then there was memorization
			# for each prompt, necessary information was deleted/one or two tiny numbers were changed
			# the point is not to test for correctness with the contamination test
			prompt = row[0]
			answer = row[1]

			completion = client.chat.completions.create(
				model=model_name.split('/')[1],
				messages=[{"role": "user", "content": prompt + "\n请通过逐步推理来解答问题，并把最终答案放置于 \\boxed{}中。"}],
                temperature=0.0,
            	max_tokens=max_length
			)
 
			response = completion.choices[0].message.content

			print(f"#### {i+1}")
			print(f"Prompt: {prompt}\n")
			print(f"Response:\n{response}\n")
			print(f"Answer: {answer}\n")

			output_file.write(f"#### {i+1}\n")
			output_file.write(f"Prompt: {prompt}\n\n")
			output_file.write(f"Response:\n\n{response}\n\n")
			output_file.write(f"Answer:{answer}\n\n")
