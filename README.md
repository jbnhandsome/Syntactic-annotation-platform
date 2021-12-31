# Syntactic annotation platform

### Description:



**12.31**

正在实现可视化依存树的功能。现在可以将每个句子的所有句法依存树都展示出来。

主要通过两个库实现了可视化的方式，第一个是通过graphiz实现的句法依存树，如下图所示：

 ![](https://i.bmp.ovh/imgs/2021/12/062f071740888914.png) 

另一个是通过spacy可视化来实现句法依存树的，如下图所示：

 ![](https://i.bmp.ovh/imgs/2021/12/85c89440af536427.png) 

图片太大显示不完全，具体的可以到dependency_tree中的output_image里面查看。



 <font color=FF0000>目前存在的问题： </font> 

1. 在spacy可视化中，当句子的长度为1时，spacy并不会将该句子可视化为语法树，而是直接显示句子中的词汇，问题如下图所示：

   ![JT`X2L8_~C`DQCW9U~_K@ZS.png](https://s2.loli.net/2021/12/31/wPNX1vbdSh9TYKF.png)

2. 在spacy可视化中，如果数据存在依赖弧交叉的情况，spacy不会可视化交叉的弧，目前来看应该是优先取消标点符号的依赖弧。问题如下图所示：

   ![7M___D_R8MVG__UX9FJXO3B.png](https://s2.loli.net/2021/12/31/FlJk5SQy8NxIGfO.png)

   我们可以看到‘！’和‘有’存在依赖关系，但是上图并没有显示。

   ![@Y_5UYR`FEHW_D9_0__V5Y2.png](https://s2.loli.net/2021/12/31/9eWzLorxaXsyPF5.png)

---

