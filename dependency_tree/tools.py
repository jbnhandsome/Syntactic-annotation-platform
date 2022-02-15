from email import header
from joblib import PrintTime
from numpy import append
from model import Conll_8best_Read
from model import Sentence
import spacy
from spacy import displacy
import os
from graphviz import Digraph
from spacy.tokens import Doc
from pathlib import Path
import requests
import json
import cairosvg

nlp = spacy.load("zh_core_web_sm")
#返回的是一个二维数组
#a['data']['url']


def load_data_conll(dataset):
    Sen = Sentence()
    sente = [Sentence() for i in range(1)]
    for i in range(len(dataset)):
        if dataset[i]:
            Sen.sen = Sen.sen + dataset[i][1]
            Sen.word.append(dataset[i][1])
            Sen.idx.append(dataset[i][0])
            Sen.tag.append(dataset[i][3])
            Sen.dep.append(dataset[i][6])
            Sen.rel.append(dataset[i][7])
            Sen.special_name.append(str(dataset[i][0])+'|'+str(dataset[i][1]+'|'+str(dataset[i][3])))
        else:
            Sen.dep_tree()
            sente.append(Sen)
            Sen = Sentence()
    del(sente[0])
    print(sente[0].sen)
    return sente
    
def find_tags(sen):
    se = set()
    for i in range(len(sen)):
        for j in range(len(sen[i].word)):
            se.add(sen[i].tag[j])
    return list(se)
def find_deps(sen):
    se = set()
    for i in range(len(sen)):
        for j in range(len(sen[i].word)):
            se.add(sen[i].rel[j])
    return list(se)

def find_sent(sen):
    se = set() #存储所有已经出现了的句子
    dic = {"":[]} #为每个句子存储所有它的index
    for i in range(len(sen)):
        if sen[i].sen not in se:
            dic[sen[i].sen]=[i] #为每个句子建立一个空集合
        else:
            continue #这个句子我们就不统计了 进行一个值的跳过
        
        for j in range(i+1,len(sen)):
            if sen[j].sen not in se and sen[i].sen == sen[j].sen: 
                dic[sen[i].sen].append(j)
        se.add(sen[i].sen)
    del(dic[""])
    return se,dic
#这个函数是用来测试是否可以生成spacy_DPtree的
# def transfer2spacy(sen):
#     for i in range(25,30):
#         #vocab = Vocab(sen[i].word)
#         #doc=Doc(vocab=vocab)
#         #转到spacy出现了一个问题，现在的结构没有存第一个root元素，这不是很好，嘶
#         #head = ['root']
#         head = [None]
#         tag = ['PU']
#         dep = ['']
#         word = ['ROOT']
#         for j in range(len(sen[i].word)):
#             #print(sen[i].dep[j],sen[i].idx[j])
#             head.append(int(sen[i].dep[j]))
#             word.append(sen[i].word[j])
#             dep.append(sen[i].rel[j])
#             tag.append(sen[i].tag[j])
#         doc = Doc(nlp.vocab,words=word,tags=tag,deps=dep,heads=head)
#         displacy.render(doc, style='dep', options = {'distance': 100})
#         for token in doc:
#             print(token.idx,token.text,token.tag_,token.dep_,token.head) # 解释标注
#生成svg图像 存储到指定位置
def generate_svg_image(path,svg):
    output_path = Path(path)
    output_path.open("w", encoding="utf-8").write(svg)
    #output_path = Path(path)
    #with output_path.open("w", encoding="utf-8") as fh:
      # fh.write(svg)
#生成graphiz类型的dependency_tree树
def generate_DPtree_graphiz(sen,st,dic,path):
    #sen是所有句子的集合，str是
    #我们需要为每一个句子生成一棵树，这里的话我们可以选择生成那个句子的树
    name = []
    for i in dic[st]:
        g = Digraph('依存树'+str(i),format='png')
        g.node(name='root')
        #需要让根节点指向0的位置
        for j in range(len(sen[i].word)):
            #如果需要添加词的属性需要加上下边这一行，否则就不需要
            #name.append(str(sen[i].word[j])+'|'+str(sen[i].tag[j]))
            g.node(sen[i].special_name[j],fontname="Microsoft YaHei")
        for j in range(len(sen[i].word)):
            if sen[i].rel[j]=='root':
                g.edge('root',sen[i].special_name[j],label=str(sen[i].dep[j]))
                
            else:
                g.edge(sen[i].Arc[sen[i].special_name[j]],sen[i].special_name[j],label=str(sen[i].rel[j]))
       # g.view()
        g.render(directory=path,view=True)

def svg2png(svg_path,png_path):
    cairosvg.svg2png(url=svg_path, write_to=png_path)

def upload(path):
    url = 'https://sm.ms/api/v2/upload'
    headers = { "Authorization": "aF5cAgMNnYr3GwFtYb3hSyMOcEjMdghT"}
    #svg2png(path,path)
    file_obj = open(path,'rb')
    file = {'smfile': file_obj}  # 参数名称必须为smfile
    data_result = requests.post(url,  files=file,headers=headers)
    print(type(data_result.json()))
    print(data_result.json())  # 得到json结果
    a= data_result.json()
    if a['success'] == False:
        return a['images']
    else:
        return a['data']['url']

#下面这个是功能代码 生成一堆句子的Dependency Tree    
def generate_DPtree_spacy(sen,dic,path):
    #sen是所有句子的集合，str是
    #我们需要为每一个句子生成一棵树
    #下面这个字典用来保存每个句子对应的句法树图片的url
    sen2spacy = []
    data_json = {}
    se = set()
    for k in range(len(sen[:28])):
        if sen[k].sen not in se:
            se.add(sen[k].sen)
            sen_list = []
            pos = 1
            for i in dic[sen[k].sen]:
                if pos>5:
                    break
                else:
                    pos = pos + 1
                head = [None]
                tag = ['PU']
                dep = ['']
                word = ['ROOT']
                #需要让根节点指向0的位置
                
                for j in range(len(sen[i].word)):
                    #print(sen[i].dep[j],sen[i].idx[j])
                    head.append(int(sen[i].dep[j]))
                    word.append(sen[i].word[j])
                    dep.append(sen[i].rel[j])
                    tag.append(sen[i].tag[j])
                doc = Doc(nlp.vocab,words=word,tags=tag,deps=dep,heads=head)
                svg = displacy.render(doc, style='dep', options = {'distance': 100,'collapse_punct':False,'fine_grained':True})
                #print("svg",svg) #这里的输出是none 存在一个bug，忘记有没有解决了，嘶
                #感觉上面的这个bug应该是在ipynb中提前渲染了，所以就没有返回值，在py中不会提前输出，所以就会存储来
                file = str(k)+str(i)+'.svg'
                output_path = path +'/'+file
                # print(output_path)
                generate_svg_image(output_path,svg)
                # #上传图片到SM.MS图床
                # url = upload(output_path)
                # sen_list.append(url)
                #上面的代码我们可以直接注释掉，可以试一下直接渲染前端页面可不可以
                sen_list.append(output_path)
            print(sen[k].sen)
            sen2spacy.append({sen[k].sen:sen_list})
    #data_json['data'] = sen2spacy
    json_s = json.dumps(sen2spacy,ensure_ascii=False)
    with open('dependency_tree\\sentence_test.json', 'w') as json_file:
        json_file.write(json_s)
    return sen2spacy
        
def generate_DPtree_ls(sen,dic,path):
    #sen是所有句子的集合，str是
    #我们需要为每一个句子生成一棵树
    #下面这个字典用来保存每个句子对应的句法树图片的url
    sen2spacy = {}
    data_json = {}
    se = set()
    #
    tags = find_tags(sen)
    rels = find_deps(sen)
    tasks = []
    
    #遍历所有的句子
    values = []
    for k in range(len(sen[0:28])):
        if sen[k].sen not in se:
            pre_dic = {}
            se.add(sen[k].sen)
            pre_dic['data']={'text':"ROOT"+sen[k].sen}
            pre_dic["predictions"] = []
            pos = 1
            value_sen = []
            print(k)
            print()
            for i in dic[sen[k].sen]:
                if pos >5:
                    break
                #print(len(dic[sen[k].sen]))
                #print(i)
                head = [0]
                tag = ['PU']
                dep = ['root']
                word = ['ROOT']
                id = [0]
                #需要让根节点指向0的位置
                for j in range(len(sen[i].word)):
                    #print(sen[i].dep[j],sen[i].idx[j])
                    id.append(j+1)
                    head.append(int(sen[i].dep[j]))
                    word.append(sen[i].word[j]) 
                    if sen[i].word[j]=='是':
                        print(sen[i].tag[j])
                    dep.append(sen[i].rel[j])#他的依赖关系
                    if sen[i].tag[j] == 'PU':
                        tag.append('PUNCT')#存储实体的属性
                    else:
                        tag.append(sen[i].tag[j])
                #每个字是一个value
                #value:{
                    #start len(word[:j-1])-1 int
                    #end   len(word[:j])-1 int 
                    #text word[j]  string
                    #labels[tags]
                #}, id:"",from_name:"tag-i",to_name:"t-i",type:"labels"
                #realation
                #{from:"from_id"
                # to:"head"
                # direction="right"
                # labels:dep
                # }
                length = 0
                for j in range(len(id)):
                    dic_v = {}
                    #先更新value
                    dic_v["value"] = {"start":length,"end":length + len(word[j]),"score": 0.70,"text":word[j],"labels":[tag[j]]}
                    length = length + len(word[j])
                    dic_v["id"]=word[j]+str(id[j])+str(pos)
                    dic_v["from_name"] = "lbl-"+str(pos)
                    dic_v["to_name"] = "txt-"+str(pos)
                    dic_v["type"] = "labels"
                    value_sen.append(dic_v)

                for j in range(len(id)):
                    if j>0:
                        dic_rel = {}
                        dic_rel["from_id"]=word[j]+str(id[j])+str(pos)
                        dic_rel["to_id"]=word[head[j]]+str(head[j])+str(pos)
                        dic_rel["type"]= "relation"
                        dic_rel["direction"]="right"
                        dic_rel["labels"] =[dep[j]]
                        #dic_rel["labels"] =[]
                        #print(dep[j])
                        value_sen.append(dic_rel)

                # file = str(k)+str(i)+'.svg'
                # output_path = path +'/'+file
                # sen_list.append(output_path)
                pos = pos + 1
            #print(sen[k].sen)
            #sen2spacy[sen[k].sen] = sen_list
            if value_sen != []:
                values.append(value_sen)
                pre_dic["predictions"].append({'result':value_sen})
                tasks.append(pre_dic) 
    #data_json['data'] = values
    json_s = json.dumps(tasks,ensure_ascii=False)
    #json_s = json.dumps(tasks)
    with open('dependency_tree\\zuixin.json', 'w',encoding='utf-8') as json_file:
        json_file.write(json_s)
    return json_s

##下面这个是测试的代码，只生成单个句子的dptree
# def generate_DPtree_spacy(sen,st,dic,path):
#     #sen是所有句子的集合，str是
#     #我们需要为每一个句子生成一棵树，这里的话我们可以选择生成那个句子的树
#     for i in dic[st]:
#         head = [None]
#         tag = ['PU']
#         dep = ['']
#         word = ['ROOT']
#         #需要让根节点指向0的位置
#         for j in range(len(sen[i].word)):
#             #print(sen[i].dep[j],sen[i].idx[j])
#             head.append(int(sen[i].dep[j]))
#             word.append(sen[i].word[j])
#             dep.append(sen[i].rel[j])
#             tag.append(sen[i].tag[j])
#         doc = Doc(nlp.vocab,words=word,tags=tag,deps=dep,heads=head)
#         svg = displacy.render(doc, style='dep', options = {'distance': 100})
#         print(type(svg))
#         file = str(i)+'.svg'
#         #utput_path = os.path.join(path,file)
#         output_path = path +'/'+file
#         print(output_path)
#         generate_svg_image(output_path,svg)
#         for token in doc:
#             print(token.idx,token.text,token.tag_,token.dep_,token.head) # 解释标注