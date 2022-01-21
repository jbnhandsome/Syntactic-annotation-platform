# Import the SDK and the client module
from label_studio_sdk import Client
import model
import tools

def ServerLaunch(url,api):
    # Define the URL where Label Studio is accessible and the API key for your user account
    LABEL_STUDIO_URL = url
    API_KEY = api
    # Connect to the Label Studio API and check the connection
    ls = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
    ls.check_connection()
    print("succeed")
    return ls

#我们这里的标签是
def create_proj(ls,sen,dic):
    #创建项目
    #数据集的格式一个字一个标签，我们现在要传入的是一句话，然后把他所有图片当作数据传入进来
    #我知道了创建一个json数据 用句子的名字作为字典的键，图片的值作为字典的值
    #<image name ='ima' value="im" valuetype="url">
    project = ls.start_project(
        title='Adonis111',
        label_config='''
        <View>
            <Header value="Select the best Dependency Tree" />
            <image name="tex" value="$im" />
            <Choices name="tag" toName="tex" >
                <Choice value="1"></Choice>
                <Choice value="2"></Choice>
                <Choice value="3"></Choice>
                <Choice value="4"></Choice>
                <Choice value="5"></Choice>
                <Choice value="6"></Choice>
                <Choice value="7"></Choice>
                <Choice value="8"></Choice>
            </Choices>
        </View>
        '''
    )
    #convert to dic
    #现在存在的问题是我们的句子是重复的，我们需要把这些句子提取出来，然后只展示不重复的句子
    #{'ids':i,'sen': sen[i].sen,'im':dic[sen[i].sen]},
    se = set()
    for i in range(len(sen[27:28])):
        #我们需要判断这个句子是否出现过
        if sen[i].sen not in se:
            se.add(sen[i].sen)
            project.import_tasks(
                [{
                    "data":{'ids':i,'sen': sen[i].sen,'im':dic[sen[i].sen]},}
                ]
            )
            
            
        else:
            continue
if __name__ == '__main__':
    LABEL_STUDIO_URL = 'http://localhost:8080'
    API_KEY = '72deb692101d5d12d3388a76580c10b730e864b0'
    
    file_path = "E:/baiduyunxiazai/zx/"
    fila_name = "notMatch.alldata"
    out_path = "dependency_tree/output_image"
    dataset = []
    data = model.Conll_8best_Read(dataset)
    dataset = data.read_mul_file(file_path,fila_name)
    sen = tools.load_data_conll(dataset)
    se,dic = tools.find_sent(sen)
    #现在我们已经有了每个句子的网络地址了 下面就需要把这些地址显示到选项中
    sen2spacy = tools.generate_DPtree_spacy(sen,dic,out_path)
    ls = ServerLaunch(LABEL_STUDIO_URL,API_KEY)
    create_proj(ls,sen,sen2spacy)

    