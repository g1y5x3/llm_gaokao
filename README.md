# curious how good LLMs are at gaokao (高考)

Source of the exams came from http://www.zizzs.com/gk/shitiku/165462.html. They were first downloaded as image format, then manually combined them 
into a single pdf file. The pdf download option from the site has too much extra stuff.

Unfortunately, currently the [pdf](data/2024_math_shanghai/exam_with_answer.pdf) file is manually converted to 
[markdown](data/2024_math_shanghai/exam_with_answer.md). I have trie [marker](https://github.com/VikParuchuri/marker) but the results were 
unusable.

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

## Preliminary evaluation based on 2024 Shanghai Math using Yi-1.5-9B-Chat ([full response](response/2024_math_shanghai.txt))

一、填空题
1. ✅ +4/4
2. ✅ +4/4
3. ✅ +4/4
4. ✅ +4/4
5. ✅ +4/4
6. ✅ +4/4
7. ✅ +5/5
8. ✅ +5/5
9. ✅ +5/5
10. ❌ +0/5
11. Skipped
12. ❌ +0/5
二、选择题
13. ✅ +4/4
14. ✅ +4/4
15. ❌ +0/5
16. ❌ +0/5
三、解答题
17. Skipped
18. (1)❌ (2)❌ +0/14
19. Skipped
20. (1)❌ (2)❌ (3)❌ +0/18
21. (1)❌ (2)❌ +0/12

    __总分.__  47/111

## TODO: 
- [] figure out how to automate grading if not considering partial credict
- [] This is just a mock test to set everything up in an efficient manner, need to test on some bigger and better models, including vision-language models for a full 150/150 grading.
- [] maybe translate into english and try again to avoid confusion/potential bugs in between `,` and `，`/ `()` and `（）`/etc. As well as spacing between chinese and english/equations. See [notes](notes.md) for more details on testing with different prompt styles.