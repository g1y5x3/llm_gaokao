# curious how good LLMs are at gaokao (高考)

Source of the exams came from http://www.zizzs.com/gk/shitiku/165462.html. They were first downloaded as image format, then manually combined into a 
single pdf file. The pdf download option from the site has too much extra stuff.

Unfortunately, currently the [pdf](data/2024_math_shanghai/exam_with_answer.pdf) file is manually converted to 
[markdown](data/2024_math_shanghai/exam_with_answer.md) (github doesn't render it well but vscode does). I have tried
[marker](https://github.com/VikParuchuri/marker) to hopefully speed-up the process but the results were not usable.

Then use `convert.py` to generate a [csv](data/2024_math_shanghai/exam_with_answer.csv) file from manually typed markdown which is used as inputs for 
the models.

```python
python llm_gaokao_test.py
```

Prompt:
```python
messages = [
    {"role": "user",   "content": "已知 $f(x) = \begin{cases}\sqrt{x}, x > 0 \\1, x \leq 0\end{cases}$，$f(3)=$"},
]
```

Response:
```text
由于函数 $f(x)$ 在 $x > 0$ 的部分定义为 $f(x) = \sqrt{x}$，因此当 $x = 3$ 时，$3 > 0$，我们可以直接使用这个定义来计算 $f(3)$。

所以，$f(3) = \sqrt{3}$。

因此，$f(3)$ 的值是 $\sqrt{3}$。
```

## Preliminary evaluation based on [2024 Shanghai Math](data/2024_math_shanghai/exam.pdf)
All model generation were configured with `temperature = 0, max_length = 4096`

Graded by hand, no partical credits. Skipped the questions that involve graph. Also skip the last question since it's hard to find a simple criteria to judge the correctness of proof.

<small>

| id (points)                                                                           | total (150) | 1 (4) | 2 (4) | 3 (4) | 4 (4) | 5 (4) | 6 (4) | 7 (5) | 8 (5) | 9 (5) | 10 (5) | 11 (5) | 12 (5) | 13 (4) | 14 (4) | 15 (5) | 16 (5) | 17 (14)  | 18 (14) | 19 (14) | 20 (18)   | 21 (18) |
| ------------------------------------------------------------------------------------- |-------------|-------|-------|-------|-------|-------|-------|-------|-------|-------|--------|--------|--------|--------|--------|--------|--------|----------|---------|---------|-----------|---------|
| [Qwen2-72B-Instruct](response/Qwen2-72B-Instruct-2024_math_shanghai.md)               |70/99        | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ❌    | Skipped | ❌    | ✅     | ✅     | ✅     | ✅     | Skipped* | ✅ ❌   | Skipped | ✅ ❌ ❌ | Skipped |
| [yi-large](response/yi-large-2024_math_shanghai.md)                                   |66/99        | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ❌    | ❌    | Skipped | ❌    | ✅     | ✅     | ✅     | ❌     | Skipped  | ❌ ✅   | Skipped | ✅ ✅ ❌ | Skipped |
| [gpt-4o](response/gpt-4o-2024_math_shanghai.md)                                       |63/99        | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ❌    | Skipped | ❌    | ✅     | ✅     | ✅     | ✅     | Skipped  | ❌ ❌   | Skipped | ✅ ❌ ❌ | Skipped |
| [Yi-1.5-34B-Chat](response/Yi-1.5-34B-Chat-2024_math_shanghai.md)                     |62/99        | ✅    | ✅    | ✅    | ✅    | ❌    | ❌    | ✅    | ✅    | ✅    | ❌    | Skipped | ❌    | ✅     | ✅     | ✅     | ✅     | Skipped  | ❌ ✅   | Skipped | ✅ ❌ ❌ | Skipped |
| [Qwen2-7B-Instruct](response/Qwen2-7B-Instruct-2024_math_shanghai.md)                 |60/99        | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ❌    | ❌    | Skipped | ❌    | ✅     | ✅     | ❌     | ✅     | Skipped  | ❌ ✅   | Skipped | ✅ ❌ ❌ | Skipped |
| [Gemini-1.5-Pro](response/gemini-1.5-pro-2024_math_shanghai.md)                       |60/99        | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ❌    | Skipped | ❌    | ✅     | ✅     | ❌     | ❌     | Skipped  | ✅ ❌   | Skipped | ✅ ❌ ❌ | Skipped |
| [Yi-1.5-9B-Chat](response/Yi-1.5-9B-Chat-2024_math_shanghai.md)                       |53/99        | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ❌    | ✅    | ✅    | ❌    | Skipped | ❌    | ✅     | ✅     | ❌     | ✅     | Skipped  | ❌ ❌   | Skipped | ✅ ❌ ❌ | Skipped |
| [Llama-3-8B-Instruct](response/Meta-Llama-3-8B-Instruct-2024_math_shanghai.md)        |36/99        | ✅    | ✅    | ❌    | ✅    | ✅    | ❌    | ❌    | ✅    | ❌    | ❌    | Skipped | ❌    | ✅     | ❌     | ❌     | ✅     | Skipped  | ❌ ❌   | Skipped | ✅ ❌ ❌ | Skipped |
| [deepseek-math-7b-instruct](response/deepseek-math-7b-instruct-2024_math_shanghai.md) |31/99        | ✅    | ✅    | ✅    | ❌    | ✅    | ✅    | ❌    | ✅    | ❌    | ❌    | Skipped | ❌    | ❌     | ❌     | ❌     | ❌     | Skipped  | ❌ ❌   | Skipped | ❌ ❌ ✅ | Skipped |
| [Mistral-7B-Instruct-v0.3](response/Mistral-7B-Instruct-v0.3-2024_math_shanghai.md)   |24/99        | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ❌    | ❌    | ❌    | ❌    | Skipped | ❌    | ❌     | ❌     | ❌     | ❌     | Skipped  | ❌ ❌   | Skipped | ❌ ❌ ❌ | Skipped |

<small>

* Qwen2-72B-Instruct was able to correctly answer 17.1 without the image. Very impressive.

## TODO: 
- [x] This is just a mock test to set everything up in an efficient manner, need to test on some bigger and better models.
- [] make the response generation as deterministic as possible for reproducibility.
- [] enable 150/150 generation and evaluation.
- [] Optimize the prompt. The answers could be very sensitive to the prompts. See [notes](notes.md) for more details on testing with different prompt styles.
