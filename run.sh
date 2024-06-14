#/bin/bash
python llm_gaokao_yi.py --model_name 01-ai/Yi-1.5-9B-Chat
python llm_gaokao_qwen.py --model_name Qwen/Qwen2-7B-Instruct
python llm_gaokao_deepseek.py --model_name deepseek-ai/deepseek-math-7b-instruct
python llm_gaokao_mistral.py
python llm_gaokao_llama.py

# # models have larger weights and may require more than 1 gpus to run
# python llm_gaokao_yi.py --model_name 01-ai/Yi-1.5-34B-Chat
# python llm_gaokao_qwen.py --model_name Qwen/Qwen2-72B-Instruct

# # models that require API keys
# python llm_gaokao_gemini.py
# python llm_gaokao_gpt4.py