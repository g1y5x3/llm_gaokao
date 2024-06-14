# curious how good LLMs are at gaokao (高考)

Source of the exams came from http://www.zizzs.com/gk/shitiku/165462.html. They were first downloaded as image format, then manually combined them 
into a single pdf file. The pdf download option from the site has too much extra stuff.

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
    {"role": "system", "content": "你要回答数学题,题目中涉及到数学表达式会以latex的方式来体现,你在回答时如果要用到数学表达式也用latex代码回复。"},
    {"role": "user", "content": "已知 k \in R, \vec{a}=(2,5), \vec{b}=(6,k), \vec{a} // \vec{b}, 则k的值为?"},
]
```

Answer:
```text
如果 \vec{a} // \vec{b}，那么 \vec{a} 和 \vec{b} 共线，即 \vec{a} 可以是 \vec{b} 的倍数，或者它们的方向向量是共线的。这里我们假设 \vec{a} 和 \vec{b} 是共线的，且 \vec{a} 是 \vec{b} 的倍数。

设 \vec{b} = x \vec{a}，其中 x 是某个实数。

将 \vec{a} 和 \vec{b} 的坐标代入，得到：

(6, k) = x (2, 5)

比较对应坐标，得到两个等式：

6 = 2x
k = 5x

从第一个等式解出 x：

x = 6 / 2 = 3

将 x 的值代入第二个等式求 k：

k = 5x = 5 * 3 = 15

因此，k 的值为 15。
```

## Preliminary evaluation based on 2024 Shanghai Math
| id (points)                                                                          | 1 (4) | 2 (4) | 3 (4) | 4 (4) | 5 (4) | 6 (4) | 7 (5) | 8 (5) | 9 (5) | 10 (5) | 11 (5) | 12 (5) | 13 (4) | 14 (4) | 15 (5) | 16 (5) | 17 (14) | 18 (14) | 19 (14) | 20 (18)   | 21 (18) | total (150) |
|-------------                                                                         |-------|-------|-------|-------|-------|-------|-------|-------|-------|--------|--------|--------|--------|--------|--------|--------|---------|---------|---------|---------  |---------|-------------|
| [Llama-3<br>8B-Instruct](response/Meta-Llama-3-8B-Instruct-2024_math_shanghai.md)    | ✅    | ✅    | ❌    | ✅    | ✅    | ❌    | ❌    | ✅    | ❌    | ❌    | Skipped | ❌    | ✅     | ❌     | ❌     | ✅     | Skipped | ❌ ❌   | Skipped | ✅ ❌ ❌ | Skipped | 36/99 |
| [Yi-1.5<br>9B-Chat](response/Yi-1.5-9B-Chat-2024_math_shanghai.md)                   | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ❌    | ❌    | Skipped | ❌    | ✅     | ✅     | ❌     | ✅     | Skipped | ❌ ❌   | Skipped | ❌ ✅ ❌ | Skipped | 53/99 |
| [Qwen2-7B-Instruct](response/Qwen2-7B-Instruct-2024_math_shanghai.md)                | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ✅    | ❌    | ❌    | Skipped | ❌    | ✅     | ✅     | ❌     | ❌     | Skipped | ❌ ❌   | Skipped | ✅ ❌ ❌ | Skipped | 48/99 |
| [deepseek-math-7b-instruct](response/deepseek-math-7b-instruct-2024_math_shanghai.md)| ✅    | ✅    | ✅    | ❌    | ✅    | ✅    | ❌    | ✅    | ❌    | ❌    | Skipped | ❌    | ❌     | ❌     | ❌     | ❌     | Skipped | ❌ ❌   | Skipped | ❌ ❌ ✅ | Skipped | 31/99 |

## TODO: 
- [] figure out how to automate grading if not considering partial credict
- [] This is just a mock test to set everything up in an efficient manner, need to test on some bigger and better models, including vision-language models for a full 150/150 grading.
- [] maybe translate into english and try again to avoid confusion/potential bugs in between `,` and `，`/ `()` and `（）`/etc. As well as spacing between chinese and english/equations. See [notes](notes.md) for more details on testing with different prompt styles.
