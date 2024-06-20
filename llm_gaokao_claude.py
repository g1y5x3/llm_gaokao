import os, csv, argparse, anthropic

parser = argparse.ArgumentParser(description="Run a model on a CSV file and save the responses.")
parser.add_argument("--model_name", default="anthropic/claude-3-5-sonnet-20240620", type=str, required=False, help="Name of the model to use.")
parser.add_argument("--max_length", default=4096, type=int, required=False, help="Maximum length for the generated response.")
parser.add_argument("--exam", default="shanghai", type=str, required=False, help="Name of the exam for the model to take.")
args = parser.parse_args()

model_name = args.model_name
exam       = args.exam
max_length = args.max_length

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

with open(f"data/2024_math_{exam}/exam_with_answer.csv", "r") as input_file:
    csv_reader = csv.reader(input_file)
    next(csv_reader)

    with open(f"response/{model_name.split('/')[1]}-2024_math_{exam}.md", "w") as output_file:
        for i, row in enumerate(csv_reader):
            prompt = row[0]
            answer = row[1]

            message = client.messages.create(
                model=model_name.split('/')[1],
                temperature=0,
                max_tokens=max_length,
                messages=[
                    {"role": "user", "content": prompt + "\n请通过逐步推理来解答问题，并把最终答案放置于 \\boxed{}中。"}
                ]
            )
            response = message.content[0].text

            print(f"#### {i+1}")
            print(f"Prompt: {prompt}\n")
            print(f"Response:\n{response}\n")
            print(f"Answer: {answer}\n")

            output_file.write(f"#### {i+1}\n")
            output_file.write(f"Prompt: {prompt}\n\n")
            output_file.write(f"Response:\n\n{response}\n\n")
            output_file.write(f"Answer:{answer}\n\n")
