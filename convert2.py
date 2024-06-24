import re
import csv
import argparse

parser = argparse.ArgumentParser(description="Run a model on a CSV file and save the responses.")
parser.add_argument("--exam", default="shanghai", type=str, required=False, help="Name of the exam for the model to take.")
args = parser.parse_args()

exam = args.exam

with open(f"data/2024_math_{exam}/exam_with_answer.md", "r") as f:
    markdown_text = f.read()

prompt_pattern = r'prompt: (.*?)(?=\n\s*answer:)'
answer_pattern = r'answer: (.*?)(?=\n\s*\d+\.\s*prompt:|\Z)'
# image_tag_pattern = re.compile(r'<img[^>]*></img>')

prompts = re.findall(prompt_pattern, markdown_text, re.DOTALL)
answers = re.findall(answer_pattern, markdown_text, re.DOTALL)

prompts = [p.strip() for p in prompts]
answers = [a.strip() for a in answers]

print(f"Number of prompts: {len(prompts)}")
print(f"Number of answers: {len(answers)}")

output_file = f"data/2024_math_{exam}/exam_with_answer.csv"
with open(output_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    writer.writerow(['prompt', 'answer'])
    for i, (prompt, answer) in enumerate(zip(prompts, answers)):
        print(f"Question {i+1}:")
        # prompt_converted = image_tag_pattern.sub('', prompt)
        print(f"Prompt: \n{prompt}")
        print(f"Answer: {answer}")
        print()
        writer.writerow([prompt, answer])

print(f"Data has been saved to {output_file}")