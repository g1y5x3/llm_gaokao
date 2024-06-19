import os, csv
from openai import OpenAI

model_name = "deepseek/deepseek-coder"
exam = "national1"

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

with open(f"data/2024_math_{exam}/exam_with_answer.csv", "r") as input_file:
	csv_reader = csv.reader(input_file)
	next(csv_reader)

	with open(f"response/{model_name.split('/')[1]}-2024_math_{exam}.md", "w") as output_file:
		for i, row in enumerate(csv_reader):
			prompt = row[0]
			answer = row[1]

			completion = client.chat.completions.create(
				model=model_name.split('/')[1],
				messages=[{"role": "user", "content": prompt + "\n请通过逐步推理来解答问题，并把最终答案放置于 \\boxed{}中。"}],
                temperature=0.0,
            	max_tokens=4096
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