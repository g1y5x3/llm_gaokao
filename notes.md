## Yi-1.5-9B-Chat
While trying to find a prompt format that works, here are some issues that I have encoutered,
1. It seems like having extra space between the chinese text and equations/english would improve the answer dramatically.
    #### prompt (Correct, but not in latex)
    ```
    messages = [
       {"role": "system", "content": "你要回答数学题,题目中涉及到数学表达式会以latex的方式来体现,你在回答时如果要用到数学表达式也用latex代码回复"},
       {"role": "user", "content": "已知抛物线 y^2=4x 上有一点 P 到准线的距离为 9 , 那么 P 到 x 轴的距离为"},
    ]
    ```
    #### answer
    ```
    ...
    所以，点 P 到 x 轴的距离为 4√2。
    ```
    [full output](https://pastebin.com/W6wq3C69)

    #### prompt (Correct, also in latex)
    ```
    messages = [
        {"role": "system", "content": "你要回答数学题, 题目中涉及到数学表达式会以latex的方式来体现, 你在回答时如果要用到数学表达式也用latex代码"},
        {"role": "user", "content": "已知抛物线 y^2=4x 上有一点 P 到准线的距离为 9, 那么 P 到 x 轴的距离为"},
    ]
    ```
    #### answer
    ```
    ...
    所以，点 P 到 x 轴的距离为 \( 4\sqrt{2} \)。
    ```
    [full output](https://pastebin.com/2xhcB20Q)    

    #### prompt (Wrong, without space)
    ```
    messages = [
       {"role": "system", "content": "你要回答数学题,题目中涉及到数学表达式会以latex的方式来体现,你在回答时如果要用到数学表达式也用latex代码回复。"},
       {"role": "user", "content": "已知抛物线y^2=4x上有一点P到准线的距离为9, 那么P到x轴的距离为?"},
    ]
    ```
    #### answer
    ```
    ...
    点P到x轴的距离就是y的绝对值：

    \[ |y| = \sqrt{\frac{4 + 4\sqrt{1361}}{17}} \]
    ```
    [full output](https://pastebin.com/TNKG2r09)

2. probably due to majority of the chinese context trained with `，` (instead of `,`), the answers were also sensitive to which comma that was used 
in the prompts 
    #### prompt (Correct, when using `，`)
    ```
    messages = [
        {"role": "system", "content": "你要回答数学题，题目中涉及到数学公式会以latex代码来表达，你在回答时如果要用到数学公式也要写成latex代码"},
        {"role": "user", "content": "已知 k \in R，\vec{a}=(2,5)，\vec{b}=(6,k)，\vec{a}//\vec{b}，则 k 的值为？"},
    ]
    ```
    #### answer
    ```
    ...
    因此，k 的值为 15。
    ```
    [full output](https://pastebin.com/Hi0LM1cD)

    #### prompt (Wrong, when using `,`)
    ```
    messages = [
        {"role": "system", "content": "你要回答数学题,题目中涉及到数学公式会以latex代码来表达,你在回答时如果要用到数学公式也要写成latex代码."},
        {"role": "user",   "content": "已知 k \in R,\vec{a}=(2,5),\vec{b}=(6,k),\vec{a}//\vec{b},则 k 的值为?"},
    ]
    ```
    #### answer
    ```
    ...
    因此，k 的值为 \sqrt{5}，即：

    k = \sqrt{5}
    ```
    [full output](https://pastebin.com/uzffp7Kg)

3. how some of the math symbols are represented also matters
    #### prompt (Correct, but based on the reasoning, seems like luck)
    ```
    messages = [
        {"role": "system", "content": "你要回答数学题，题目中涉及到数学公式会以latex代码来表达，你在回答时如果要用到数学公式也要写成latex代码。"},
        {"role": "user",   "content": "定义一个集合 \Omega，集合元素是空间内的点集，任取 P_1, P_2, P_3 \in \Omega，存在不完全为 0 的实数 \lambda_1, \lambda_2, \lambda_3，使得 \lambda_1 OP_1 + \lambda_2 OP_2 + \lambda_3 OP_3 = 0。 已知 (1,0,0) \in \Omega，则 (0,0,1) \not\in \Omega 的充分条件是？ A. (0,0,0) B. (-1,0,0) C. (0,1,0) D. (0,0,-1)"},
    ]
    ```
    #### answer
    ```
    ...
    因此，(0,0,1) \notin \Omega 的充分条件是 C. (0,1,0)。
    ```
    [full output](https://pastebin.com/R79Y9c4e)

    #### prompt (Wrong, the only difference was `\notin` instead of `\not\in`)
    ```
    messages = [
        {"role": "system", "content": "你要回答数学题，题目中涉及到数学公式会以latex代码来表达，你在回答时如果要用到数学公式也要写成latex代码。"},
        {"role": "user",   "content": "定义一个集合 \Omega，集合元素是空间内的点集，任取 P_1, P_2, P_3 \in \Omega，存在不完全为 0 的实数 \lambda_1, \lambda_2, \lambda_3，使得 \lambda_1 OP_1 + \lambda_2 OP_2 + \lambda_3 OP_3 = 0。 已知 (1,0,0) \in \Omega，则 (0,0,1) \notin \Omega 的充分条件是？ A. (0,0,0) B. (-1,0,0) C. (0,1,0) D. (0,0,-1)"},
    ]
    ```
    #### answer
    ```
    根据题意，集合 \Omega 中的元素是空间内的点集。我们要求出 (0,0,1) \in \Omega 的充分条件。
    ...
    因此，(0,0,1) \notin \Omega 的充分条件是 C. (0,1,0)。
    ```
    [full output](https://pastebin.com/qURjeaCe)

4. model sometimes fail with less prompts
    #### prompt (only the first question was given, however, with `max_length`=8192, it was not able to finish the answer)
    ```
    messages = [
        {"role": "system", "content": "你要回答数学题，题目中涉及到数学公式会以latex代码来表达，你在回答时如果要用到数学公式也要写成latex代码。"},
        {"role": "user",   "content": "双曲线 \Tau: x^2 - \frac{y^2}{b^2} = 1，(b>0)，A_1，A_2 为左右定点，过点 M(-2,0) 的直线 l 交双曲线 T 于两点 P、Q，且点 P 在第一象限，（1）若 e=2 时，求b？"},
    ]
    ```
    #### answer (exceed 8192 maximum length, the last part seems to be very random)
    [full output](https://pastebin.com/WMmX0hGX)

    #### prompt (if all 3 questions were provided, the answer seems to be more reasonable and concise, `max_length`=4096)
    ```
    messages = [
        {"role": "system", "content": "你要回答数学题，题目中涉及到数学公式会以latex代码来表达，你在回答时如果要用到数学公式也要写成latex代码。"},
        {"role": "user",   "content": "双曲线 \Tau: x^2 - \frac{y^2}{b^2} = 1，(b>0)，A_1，A_2 为左右定点，过点 M(-2,0) 的直线 l 交双曲线 T 于两点 P、Q，且点 P 在第一象限，（1）若 e=2 时，求b？（2）若 b=\frac{2\sqrt{6}}{3}，\triangle MA_2P 为等腰三角形时，求 P 的坐标？ （3）过点 Q 作 OQ 延长线交 \Tau 于点 R，若 \vec{A_1R} \cdot \vec{A_2P} = 1，求 b 取值范围？"},
    ]
    ```
    #### answer (got the first one right)
    ```
    ...
    因此，当 e = 2 时，b 的值为 √3。
    ...
    因此，P 的坐标为 (x_p, y_p) = (\frac{1}{2}, \frac{2\sqrt{6}}{3})。
    ...
    因此，b 的取值范围为 (0, 1]。
    ```
    [full output](https://pastebin.com/N3qi4Tac)