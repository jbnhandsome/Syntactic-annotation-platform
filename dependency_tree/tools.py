from model import Conll_8best_Read
from model import Sentence
import spacy
from spacy import displacy
import os
from graphviz import Digraph
from spacy.tokens import Doc
from pathlib import Path
nlp = spacy.load("zh_core_web_sm")

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
#用来测试 不会在正式版出现    
def transfer2spacy(sen):
    for i in range(25,30):
        #vocab = Vocab(sen[i].word)
        #doc=Doc(vocab=vocab)
        #转到spacy出现了一个问题，现在的结构没有存第一个root元素，这不是很好，嘶
        #head = ['root']
        head = [None]
        tag = ['PU']
        dep = ['']
        word = ['ROOT']
        for j in range(len(sen[i].word)):
            #print(sen[i].dep[j],sen[i].idx[j])
            head.append(int(sen[i].dep[j]))
            word.append(sen[i].word[j])
            dep.append(sen[i].rel[j])
            tag.append(sen[i].tag[j])
        doc = Doc(nlp.vocab,words=word,tags=tag,deps=dep,heads=head)
        displacy.render(doc, style='dep', options = {'distance': 100})
        for token in doc:
            print(token.idx,token.text,token.tag_,token.dep_,token.head) # 解释标注
#生成svg图像 存储到指定位置
def generate_svg_image(path,svg):
    output_path = Path(path)
    with output_path.open("w", encoding="utf-8") as fh:
        fh.write(svg)

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
def generate_DPtree_spacy(sen,st,dic,path):
    #sen是所有句子的集合，str是
    #我们需要为每一个句子生成一棵树，这里的话我们可以选择生成那个句子的树
    for i in dic[st]:
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
        svg = displacy.render(doc, style='dep', options = {'distance': 100})
        print(type(svg))
        file = str(i)+'.svg'
        #utput_path = os.path.join(path,file)
        output_path = path +'/'+file
        print(output_path)
        generate_svg_image(output_path,svg)
        for token in doc:
            print(token.idx,token.text,token.tag_,token.dep_,token.head) # 解释标注