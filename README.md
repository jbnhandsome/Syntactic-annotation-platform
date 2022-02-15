# Syntactic annotation platform

## Description:

在句法标注任务中，针对同一个句子，我们可能有多种句法标注的方法，并且会为这个句子生成多种句法依存树。为了更好的观察句法标注的结果是否正确，我们使用了<a href="https://labelstud.io/">Label-Studio</a> 开发这个项目。

**功能简介：**

目前的功能包括数据导入和结果导出，可视化依赖关系与标签, 可视化依存树。

**项目界面展示图：**

![image.png](https://s2.loli.net/2022/02/15/G4h27QOarYD3ktW.png)

![image.png](https://s2.loli.net/2022/02/15/imKfgPecF63GHAS.png)



### Dependencies

Django==3.1.13
graphviz==0.19.1
joblib==1.0.1
label_studio_sdk==0.0.6
numpy==1.21.5
requests==2.26.0
spacy==3.2.1

```
pip install -r requirements.txt
```



## Usage

这个项目使用了anaconda来管理环境。

配置文件都放在config.json中

```
{"LABEL_STUDIO_URL" : "http://localhost:8080", 
    "API_KEY" :"83443f95363aaaa600059c7c41db23164d04eb58",
    "file_path" : "E:/data/best_8/",
    "fila_name" : "notMatch.alldata",
    "out_path" : "dependency_tree\\output_image",
    "outfile_path":"dependency_tree\\output_file",
    "n" : 5
}
```

LABEL_STUDIO_URL : host

API_KEY : Label-Studio 的API

file_path: 存放数据的地址

fila_name：数据的名称

out_path : 生成的依存关系的存储地址

outfile_path : 标注结束后，生成的结果存放地址

n : 每个句子生成的依赖树的数目



**启动 :** 

```
label-studio start
cd 你的project地址
python server.py
```

