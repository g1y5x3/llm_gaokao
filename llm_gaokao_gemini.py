import google.generativeai as genai
import os, csv, argparse

parser = argparse.ArgumentParser(description="Run a model on a CSV file and save the responses.")
parser.add_argument("--model_name", default="google/gemini-1.5-pro", type=str, required=False, help="Name of the model to use.")
parser.add_argument("--max_length", default=4096, type=int, required=False, help="Maximum length for the generated response.")
parser.add_argument("--exam", default="shanghai", type=str, required=False, help="Name of the exam for the model to take.")
args = parser.parse_args()

model_name = args.model_name
exam       = args.exam
max_length = args.max_length

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(model_name.split('/')[1])

generation_config = genai.GenerationConfig(
    temperature=0.0,
    max_output_tokens=max_length
)

with open(f"data/2024_math_{exam}/exam_with_answer.csv", "r") as input_file:
    csv_reader = csv.reader(input_file)
    next(csv_reader)

    with open(f"response/{model_name.split('/')[1]}-2024_math_{exam}.md", "w") as output_file:
        for i, row in enumerate(csv_reader):
            prompt = row[0]
            answer = row[1]

            response = model.generate_content(prompt + "\n请通过逐步推理来解答问题，并把最终答案放置于 \\boxed{}中。",
                                              generation_config=generation_config)

            print(f"#### {i+1}")
            print(f"Prompt: {prompt}\n")
            print(f"Response:\n{response.text}\n")
            print(f"Answer: {answer}\n")

            output_file.write(f"#### {i+1}\n")
            output_file.write(f"Prompt: {prompt}\n\n")
            output_file.write(f"Response:\n\n{response.text}\n\n")
            output_file.write(f"Answer:{answer}\n\n")