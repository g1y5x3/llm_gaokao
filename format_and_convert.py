import re, csv, argparse

parser = argparse.ArgumentParser(description="Select the exam to convert to csv.")
parser.add_argument("--exam", default="shanghai", type=str, required=False, help="Name of the exam.")
args = parser.parse_args()
exam = args.exam

def format_equations_and_punctuation(text):
    if re.search(r'\S\$|\$\S|\$\s.*?\s\$', text) is not None:
        # Add spaces around $$ equations
        text = re.sub(r'(\S)(\$)', r'\1 \2', text)
        text = re.sub(r'(\$)(\S)', r'\1 \2', text)
        text = re.sub(r'\$\s*(.*?)\s*\$', r'$\1$', text)
    
    # Replace English punctuation with Chinese punctuation
    punctuation_map = {
        ',': '，',
        '?': '？', 
        '.': '。',
        '（': '(',
        '）': ')',
    }

    for eng, chi in punctuation_map.items():
        text = text.replace(eng, chi)

    multiple_choice_correction = {
        'A。 ': 'A.',
        'B。 ': 'B.', 
        'C。 ': 'C.',
        'D。 ': 'D.',
    }

    for bef, aft in multiple_choice_correction.items():
        text = text.replace(bef, aft)
    
    return text

with open(f"data/2024_math_{exam}/exam_with_answer.md", "r") as f:
    markdown_text = f.read()

prompt_pattern = r'prompt: (.*?)\n'
answer_pattern = r'answer: (.*?)\n'

# not doing anything currently for later evaluating models with vision capabilities
image_tag_pattern = re.compile(r'<img[^>]*></img>')

formatted_text = format_equations_and_punctuation(markdown_text)

prompts = re.findall(prompt_pattern, formatted_text, re.DOTALL)
print(len(prompts))
answers = re.findall(answer_pattern, formatted_text, re.DOTALL)
print(len(answers))

output_file = f"data/2024_math_{exam}/exam_with_answer.csv"
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
