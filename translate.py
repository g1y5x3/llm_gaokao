import os, csv, argparse, anthropic

parser = argparse.ArgumentParser(description="Run a model on a CSV file and save the responses.")
parser.add_argument("--model_name", default="anthropic/claude-3-5-sonnet-20240620", type=str, required=False, help="Name of the model to use.")
parser.add_argument("--exam", default="shanghai", type=str, required=False, help="Name of the exam for the model to take.")
args = parser.parse_args()

model_name = args.model_name
exam       = args.exam

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

with open(f"data/2024_math_{exam}/exam_with_answer.csv", "r") as input_file:
    csv_reader = csv.reader(input_file)
    next(csv_reader)


    with open(f"data/2024_math_{exam}/exam_with_answer_english.csv", "w", newline='', encoding='utf-8') as output_file:
        writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
        writer.writerow(['prompt', 'answer'])
        for i, row in enumerate(csv_reader):
            prompt = row[0]
            answer = row[1]

            message = client.messages.create(
                model=model_name.split('/')[1],
                messages=[{"role": "user", "content": prompt + "\nPlease translate the question into Enlgish. Keep the equations wrapped in $. Please do not include any additional notes or explainations. And do not include any additional statements at the beginning either."}],
                temperature=0,
                max_tokens=4096
            )
            response = message.content[0].text

            print(f"#### {i+1}")
            print(f"Prompt: {prompt}\n")
            print(f"Response:\n{response}\n")
            print(f"Answer: {answer}\n")

            writer.writerow([response, answer])
