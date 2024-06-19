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

## Evaluation based on [2024 Shanghai Math](data/2024_math_shanghai/exam.pdf) and [2024 National1 Math](data/2024_math_national1/exam_with_answer.pdf)
All model generation were configured with `temperature = 0`, and `max_length = 4096`

Graded by hand, no partial credits. Skipped the questions that involve image/graph/table understanding. Also skip the last question since it's hard to find a simple criteria to judge the correctness of proof.

| model                     | national1 | shanghai |
|---------------------------|-----------|----------|
| deepseek-coder            | 58/106    | 82/99    |
| Qwen2-72B-Instruct        |           | 70/99    |
| yi-large                  |           | 66/99    |
| gpt-4o                    |           | 63/99    |
| Yi-1.5-34B-Chat           |           | 62/99    |
| Qwen2-7B-Instruct         |           | 60/99    |
| Gemini-1.5-Pro            |           | 60/99    |
| Yi-1.5-9B-Chat            |           | 53/99    |
| Llama-3-70B-Instruct      |           | 49/99    |
| deepseek-chat(v2)         |           | 44/99    |
| Llama-3-8B-Instruct       |           | 36/99    |
| deepseek-math-7b-instruct |           | 31/99    |

_itemization of grades can be found in this [spreadsheet](https://docs.google.com/spreadsheets/d/1I4Qi6-ad34KQlryBkRMNSGbEBU05dz4OcRs-AniWwLM/edit?gid=0#gid=0)_

## TODO: 
- [x] This is just a mock test to set everything up in an efficient manner, need to test on some bigger and better models.
- [x] make the response generation as deterministic as possible for reproducibility.
- [ ] add the rest of math exams
- [ ] enable 150/150 generation and evaluation.
- [ ] Optimize the prompt. The answers could be very sensitive to the prompts. See [notes](notes.md) for more details on testing with different prompt styles.
