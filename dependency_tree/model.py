import os

class Conll_8best_Read():
    def __init__(self,dataset):
        self.dataset=dataset
    #这个函数没测试过 不过多个的没问题，这个应该也没啥问题
    def read_single_file(self,file_path,file_name):
        #path = E:\\baiduyunxiazai\\zx
        #file_path = "E:\\baiduyunxiazai\\zx\\top1\\notMatch.1"
        paths=['top1','top2','top3','top4','top5','top6','top7','top8']
        #file_path = "E:\\baiduyunxiazai\\zx\\top1\\notMatch.1"
        #file_path+paths[j]+notMatch.alldata
        file = os.path.join(file_path,paths[0],file_name)
        with open(file,'r', encoding='utf-8') as fb:
            for line in fb:
                line = line.strip('\n') 
                if line:
                    self.dataset.append(line.split('\t'))
                else:
                    self.dataset.append([])
        return self.dataset
         
    def read_mul_file(self,file_path,file_name):
        #一共973句话 算上']'
        #path = E:\\baiduyunxiazai\\zx
        paths=['top1','top2','top3','top4','top5','top6','top7','top8']
        #file_path = "E:\\baiduyunxiazai\\zx\\top1\\notMatch.1"
        for j in range(8):
            #file_path+paths[j]+notMatch.alldata
            file = os.path.join(file_path,paths[j],file_name)
            print(file)
            with open(file,'r', encoding='utf-8') as fb:
                for line in fb:
                    line = line.strip('\n') 
                    if line:
                        self.dataset.append(line.split('\t'))
                    else:
                        self.dataset.append([])
        return self.dataset
         

class Sentence(object):
    def __init__(self):
        self.sen = "" #用来判断句子是否相同
        self.idx= [] #存每一个单词的序号
        self.word = [] #存每一个单词
        self.tag = [] #存储标签
        self.dep = [] #存储依赖
        self.rel = [] #依赖关系
        self.Arc={} #字典
        self.special_name=[]
        
    def equal(self,a,b):
        if a == b:
            return True
        else:
            return False
    def dep_tree(self):
        #这里面把所有的弧都取出来
        for i in range(len(self.word)):
            if self.dep[i] == '0':
                self.Arc[self.special_name[i]] = 'root'
            else:
                for j in range(len(self.word)):
                    if self.idx[j] == self.dep[i]:
                        self.Arc[self.special_name[i]] = self.special_name[j]
                
            
