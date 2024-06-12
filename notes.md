## Yi-1.5-9B-Chat
1. It seems like having extra space between the chinese text and equations/english would improve the answer dramatically.
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
    for the entire [output](https://pastebin.com/W6wq3C69)

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
    for the entire [output](https://pastebin.com/2xhcB20Q)    

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
    for the entire [output](https://pastebin.com/TNKG2r09)