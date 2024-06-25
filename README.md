# curious how good LLMs are at gaokao (高考)

## Data Collection
Source of the exams came from http://www.zizzs.com/gk/shitiku/165462.html. They were first downloaded as image format, then manually combined into a
single pdf file. The pdf download option from the site has too much extra stuff.

Unfortunately, currently the [pdf](data/2024_math_shanghai/exam_with_answer.pdf) files are semi-manually converted to [markdown](data/2024_math_shanghai/exam_with_answer.md) (github doesn't render it well but vscode does). I have tried [marker](https://github.com/VikParuchuri/marker) to hopefully speed-up the process but the results were not usable. Probably due to the model was trained on mostly vectorized pdf data with much higher resolution. In this case, the exam pdf files were converted from jpg/png so the resolution is much smaller.

Then use `convert.py` to generate a [csv](data/2024_math_shanghai/exam_with_answer.csv) file from manually typed markdown which is used as inputs for
the models.

## Eval example
#### Prompt:
```python
messages = [
    {"role": "user",   "content": "已知 $f(x) = \begin{cases}\sqrt{x}, x > 0 \\1, x \leq 0\end{cases}$，$f(3)=$"},
]
```

#### Response (from Yi-1.5-9B-Chat):
```text
由于函数 $f(x)$ 在 $x > 0$ 的部分定义为 $f(x) = \sqrt{x}$，因此当 $x = 3$ 时，$3 > 0$，我们可以直接使用这个定义来计算 $f(3)$。

所以，$f(3) = \sqrt{3}$。

因此，$f(3)$ 的值是 $\sqrt{3}$。
```
## Question Formatting rules
All of the rules were based purely on observations. They are experimental and could lead to a pretty big variation in terms of model responses.
Unfortunately this is also the biggest pain point of evaluating these models due to being closely related to BPE.
1. Insert ` ` before and after `$` for equations and numbers.
2. Use language specific punctuation characters - `，。？` for Chinese and `,.?` for English except within the equations.
3. Use `newline` character for multiple choice questions and comprehensive questions.

### TODO: add some examples to illustrate this problem

## Evaluations (graded by hand)
All model generation were configured with `temperature = 0`, and `max_length = 4096`

No partial credits and questions that involve image/graph/table understanding as well as proof are skipped.

### Prompted in Chinese
| model              | shanghai  | beijing   | national1  | national2  |
|--------------------|-----------|-----------|------------|------------|
| deepseek-coder     |   77/99   |   57/133  |   63/106   |   92/118   |
| claude-3-5-sonnet  |   52/99   |   53/133  |   55/106   |   65/118   |
<!-- | gpt-4o             |   53/99   |           |           |   61/106   |   63/118   |            |            | -->
<!-- | Gemini-1.5-pro     |   60/99   |           |           |   54/106   |   63/118   |            |            | -->
<!-- | Qwen2-72B-Instruct |   63/99   |           |           |   62/106   |   59/118   |            |            | -->
<!-- | yi-large           |   44/99   |           |           |   41/106   |   55/118   |            |            | -->

### Prompted in English
| model              | shanghai  | beijing   | national1  | national2  |
|--------------------|-----------|-----------|------------|------------|
| deepseek-coder     |   60/99   |   61/133  |   63/106   |   74/118   |
| claude-3-5-sonnet  |   65/99   |   34/133  |   54/106   |   71/118   |
<!-- | gpt-4o             |           |           |           |            |            |            |            | -->
<!-- | Gemini-1.5-pro     |           |           |           |            |            |            |            | -->
<!-- | Qwen2-72B-Instruct |           |           |           |            |            |            |            | -->
<!-- | yi-large           |           |           |           |            |            |            |            | -->


_itemization of grades can be found in this [spreadsheet](https://docs.google.com/spreadsheets/d/1I4Qi6-ad34KQlryBkRMNSGbEBU05dz4OcRs-AniWwLM/edit?gid=0#gid=0)_

## TODO:
- [x] This is just a mock test to set everything up in an efficient manner, need to test on some bigger and better models.
- [x] make the response generation as deterministic as possible for reproducibility.
- [x] manually format all questions (actually the format is almost automated through better prompting claude 3.5 to extract the texts).
- [ ] add the rest of math exam
- [ ] automate the benchmark scoring.
- [ ] enable 150/150 generation and evaluation.
- [ ] Optimize the prompt. The answers could be very sensitive to the prompts. See [notes](notes.md) for more details on testing with different prompt styles.
