# curious how good LLMs are at gaokao (高考)

Source of the exams came from http://www.zizzs.com/gk/shitiku/165462.html. They were first downloaded as image format, then manually combined them 
into a single pdf file. The pdf download option from the site has too much extra stuff.

Unfortunately, currently the [pdf](data/2024/math/shanghai/exam_with_answer.pdf) file is manually converted to 
[markdown](data/2024/math/shanghai/exam_with_answer_chinese.md). I have trie [marker](https://github.com/VikParuchuri/marker) but the results were 
unusable.

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