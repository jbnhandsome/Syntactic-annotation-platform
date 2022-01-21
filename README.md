# Syntactic annotation platform

### Description:



**12.31**

正在实现可视化依存树的功能。现在可以将每个句子的所有句法依存树都展示出来。

主要通过两个库实现了可视化的功能，第一个是通过graphiz实现的句法依存树，如下图所示：

 ![](https://i.bmp.ovh/imgs/2021/12/062f071740888914.png) 

第二个是通过spacy可视化来实现句法依存树的，如下图所示：

  ![WUT_B_GP2_L@_9_HQK10__T.png](https://s2.loli.net/2022/01/02/yCvtYV9XFq1w3P6.png)



**1.17**

**工作进展：**

1. 学习label-studio
2. 尝试搭建demo
3. 更新了上传图片到图床的功能
![1642416017_1_.png](https://s2.loli.net/2022/01/17/btXwCgDM435cVqB.png)

**存在问题：**
![1642416940_1_.png](https://s2.loli.net/2022/01/17/PEHqyT6hVZoMjBp.png)

1. label-studio好像不支持在选项中显示图片。就是假设现在有800个句子，每个句子我为他生成了5-8棵语法树，我把这些语法树存到图床上了，并存下来他们的url。现在我希望把这些url传到label-studio的选项里展示，但是label-studio似乎并不支持这种方式。
2. 在label-studio-fronted前端模板中，选项是要预先设定的，不能根据每个句子有几颗语法树进行更改。比如说对上图这一句话，我们有八棵Denpendency Tree，但是对别的句子我们可能只有五棵语法树，这个选项是没法变化的。

---

