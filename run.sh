#/bin/bash
python llm_gaokao_yi.py
python llm_gaokao_qwen.py --model_name Qwen/Qwen2-7B-Instruct --max_length 4096
# python llm_gaokao_qwen.py --model_name Qwen/Qwen2-72B-Instruct --max_length 4096
python llm_gaokao_deepseek.py
python llm_gaokao_mistral.py
python llm_gaokao_llama.py
# python llm_gaokao_gemini.py
# python llm_gaokao_gpt4.py
