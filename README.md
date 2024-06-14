# curious how good LLMs are at gaokao (高考)

Source of the exams came from http://www.zizzs.com/gk/shitiku/165462.html. They were first downloaded as image format, then manually combined into a 
single pdf file. The pdf download option from the site has too much extra stuff.

Unfortunately, currently the [pdf](data/2024_math_shanghai/exam_with_answer.pdf) file is manually converted to 
[markdown](data/2024_math_shanghai/exam_with_answer.md) (github doesn't render it well but vscode does). I have trie 
[marker](https://github.com/VikParuchuri/marker) to speed-up the process but the results were not usable.

Then use `convert.py` to generate a [csv](data/2024_math_shanghai/exam_with_answer.csv) file from manually typed markdown which is used as inputs for 
the models. This conversion removes all the `$$` for latex display as well as handles image tags. 

```python
python llm_gaokao_test.py
```

Question:
```python
messages = [
    {"role": "user",   "content": "已知抛物线 $y^2=4x$ 上有一点 $P$ 到准线的距离为 9， 那么 $P$ 到 $x$ 轴的距离为？"},
]
```

Answer:
```text
首先，我们需要知道抛物线的标准方程和性质。给定的抛物线方程是 $y^2=4x$，这是一个右开口的抛物线，其焦点在 $x$-轴上，准线是一条与抛物线对称的直线。

对于右开口的抛物线 $y^2=4px$，其中 $p$ 是抛物线的焦距，即焦点到准线的距离。在这个例子中，$p=1$。

根据抛物线的性质，任何点 $P(x, y)$ 在抛物线上到准线的距离等于它到焦点的距离。给定的点 $P$ 到准线的距离为 9，因此 $P$ 到焦点的距离也是 9。

由于 $p=1$，焦点的坐标为 $(p, 0) = (1, 0)$。因此，从点 $P$ 到焦点 $(1, 0)$ 的距离为 9。

现在，我们需要找到点 $P$ 的坐标。由于 $P$ 在抛物线上，它的坐标满足方程 $y^2=4x$。同时，根据抛物线的定义，点 $P$ 到焦点 $(1, 0)$ 的距离为 9，即：

\[ \sqrt{(x-1)^2 + y^2} = 9 \]

将 $y^2=4x$ 代入上述方程，我们得到：

\[ \sqrt{(x-1)^2 + 4x} = 9 \]

平方两边得到：

\[ (x-1)^2 + 4x = 81 \]

展开并简化方程：

\[ x^2 - 2x + 1 + 4x = 81 \]
\[ x^2 + 2x + 1 = 81 \]
\[ x^2 + 2x - 80 = 0 \]

这是一个二次方程，我们可以解它来找到 $x$ 的值。使用因式分解，我们得到：

\[ (x + 10)(x - 8) = 0 \]

因此，$x = -10$ 或 $x = 8$。由于抛物线 $y^2=4x$ 的定义域为 $x \geq 0$，我们取 $x = 8$。

对于 $x = 8$，代入 $y^2=4x$ 得到：

\[ y^2 = 4 \times 8 = 32 \]

所以 $y = \pm \sqrt{32} = \pm 4\sqrt{2}$。

因此，点 $P$ 的坐标是 $(8, 4\sqrt{2})$ 或 $(8, -4\sqrt{2})$。

点 $P$ 到 $x$ 轴的距离是 $y$ 坐标的绝对值，即 $|4\sqrt{2}| = 4\sqrt{2}$。

所以，点 $P$ 到 $x$ 轴的距离为 $4\sqrt{2}$。
```

## Preliminary evaluation based on 2024 Shanghai Math
| id (points)                                                                           | 1 (4) | 2 (4) | 3 (4) | 4 (4) | 5 (4) | 6 (4) | 7 (5) | 8 (5) | 9 (5) | 10 (5) | 11 (5) | 12 (5) | 13 (4) | 14 (4) | 15 (5) | 16 (5) | 17 (14) | 18 (14) | 19 (14) | 20 (18)   | 21 (18) | total (150) |
| ------------------------------------------------------------------------------------- |-------|-------|-------|-------|-------|-------|-------|-------|-------|--------|--------|--------|--------|--------|--------|--------|---------|---------|---------|-----------|---------|-------------|
| [Qwen2-7B-Instruct](response/Qwen2-7B-Instruct-2024_math_shanghai.md)                 | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ❌    | ❌    | Skipped | ❌    | ✅     | ✅     | ❌     | ✅     | Skipped | ❌ ✅   | Skipped | ✅ ❌ ❌ | Skipped | 60/99 |
| [Yi-1.5-9B-Chat](response/Yi-1.5-9B-Chat-2024_math_shanghai.md)                    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ❌    | ✅    | ✅    | ❌    | Skipped | ❌    | ✅     | ✅     | ❌     | ✅     | Skipped | ❌ ❌   | Skipped | ✅ ❌ ❌ | Skipped | 53/99 |
| [Llama-3-8B-Instruct](response/Meta-Llama-3-8B-Instruct-2024_math_shanghai.md)     | ✅    | ✅    | ❌    | ✅    | ✅    | ❌    | ❌    | ✅    | ❌    | ❌    | Skipped | ❌    | ✅     | ❌     | ❌     | ✅     | Skipped | ❌ ❌   | Skipped | ✅ ❌ ❌ | Skipped | 36/99 |
| [deepseek-math-7b-instruct](response/deepseek-math-7b-instruct-2024_math_shanghai.md) | ✅    | ✅    | ✅    | ❌    | ✅    | ✅    | ❌    | ✅    | ❌    | ❌    | Skipped | ❌    | ❌     | ❌     | ❌     | ❌     | Skipped | ❌ ❌   | Skipped | ❌ ❌ ✅ | Skipped | 31/99 |
| [Mistral-7B-Instruct-v0.3](response/Mistral-7B-Instruct-v0.3-2024_math_shanghai.md)   | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ❌    | ❌    | ❌    | ❌    | Skipped | ❌    | ❌     | ❌     | ❌     | ❌     | Skipped | ❌ ❌   | Skipped | ❌ ❌ ❌ | Skipped | 24/99 |

## TODO: 
- [] figure out how to automate grading if not considering partial credict
- [x] This is just a mock test to set everything up in an efficient manner, need to test on some bigger and better models, including vision-language models for ~~a full 150/150 grading~~ grade the last question is kinda hard.
- [] maybe translate into english and try again to avoid confusion/potential bugs in between `,` and `，`/ `()` and `（）`/etc. As well as spacing between chinese and english/equations. See [notes](notes.md) for more details on testing with different prompt styles.
