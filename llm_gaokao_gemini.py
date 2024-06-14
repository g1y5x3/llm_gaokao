import google.generativeai as genai
import os, csv

model_name = "google/gemini-1.5-pro"
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')


with open("data/2024_math_shanghai/exam_with_answer.csv", "r") as input_file:
    csv_reader = csv.reader(input_file)
    next(csv_reader)

    with open(f"response/{model_name.split('/')[1]}-2024_math_shanghai.md", "w") as output_file:
        for i, row in enumerate(csv_reader):
            prompt = row[0]
            answer = row[1]

            response = model.generate_content(prompt + "\n请通过逐步推理来解答问题，并把最终答案放置于 \\boxed{}中。")

            print(f"#### {i+1}")
            print(f"Prompt: {prompt}\n")
            print(f"Response:\n{response.text}\n")
            print(f"Answer: {answer}\n")

            output_file.write(f"#### {i+1}\n")
            output_file.write(f"Prompt: {prompt}\n\n")
            output_file.write(f"Response:\n\n{response.text}\n\n")
            output_file.write(f"Answer:{answer}\n\n")