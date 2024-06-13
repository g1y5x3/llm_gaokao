import re
import csv

with open("data/2024_math_shanghai/exam_with_answer.md", "r") as f:
    markdown_text = f.read()

prompt_pattern = r'prompt: (.*?)\n'
answer_pattern = r'answer: (.*?)\n'
image_tag_pattern = re.compile(r'<img[^>]*></img>')

prompts = re.findall(prompt_pattern, markdown_text, re.DOTALL)
answers = re.findall(answer_pattern, markdown_text, re.DOTALL)

output_file = "data/2024_math_shanghai/exam_with_answer.csv"
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    writer.writerow(['prompt', 'answer'])
    for i, (prompt, answer) in enumerate(zip(prompts, answers)):
        print(i+1)
        prompt_converted = image_tag_pattern.sub('', prompt)
        print(prompt_converted)
        print(answer)
        print()
        writer.writerow([prompt_converted, answer])

print(f"Data has been saved to {output_file}")
