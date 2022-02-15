# Import the SDK and the client module
import json
from django import conf
from label_studio_sdk import Client
import model
import tools
import os

def ServerLaunch(url,api):
    # Define the URL where Label Studio is accessible and the API key for your user account
    LABEL_STUDIO_URL = url
    API_KEY = api
    # Connect to the Label Studio API and check the connection
    ls = Client(url=LABEL_STUDIO_URL, api_key=API_KEY)
    #ls.make_request()
    ls.check_connection()
    print("succeed")
    return ls

#我们这里的标签是
def create_proj(ls,sen,tasks,n):
    
    # 'SP', 'VE', 'IJ', 'SB', 'DEG', 'BA', 'DT', 'JJ', 'OD', 'AS', 'PN', 'DEV', 'CS', 'NT', 'CD',
    #  'VA', 'ETC', 'NR', 'DEC', 'DER', 'NN', 'LB', 'PUNCT', 'P', 'MSP', 'CC', 'M', 'VVN', 'LC', 'VC', 'AD', 'ON', 'VV'
    label_ralation = """<Relations>
                <Relation value="root" /><Relation value="dfsubj" /><Relation value="adv" /><Relation value="de" /><Relation value="sasubj-obj" />
                <Relation value="app" /><Relation value="att" /><Relation value="pred" /><Relation value="subj" /><Relation value="sasubj" />
                <Relation value="punc" /><Relation value="pobj" /><Relation value="cmp" /><Relation value="obj" /><Relation value="iobj" />
                <Relation value="repet" /><Relation value="adjct" /><Relation value="coo" /><Relation value="subj-in" />
            </Relations>"""
    label_tags="""<Label value="SP" /><Label value="VE" /><Label value="IJ" /><Label value="SB" /><Label value="DEG" /><Label value="BA" />
                <Label value="DT" /><Label value="JJ" /><Label value="OD" /><Label value="AS" /><Label value="PN" /><Label value="DEV" />
                <Label value="CS" /><Label value="NT" /><Label value="CD" /><Label value="VA" /><Label value="ETC" /><Label value="NR" />
                <Label value="DEC" /><Label value="DER" /><Label value="NN" /><Label value="LB" /><Label value="PUNCT" /><Label value="P" />
                <Label value="MSP" /><Label value="CC" /><Label value="M" /><Label value="VVN" /><Label value="LC" /><Label value="AD" />
                <Label value="ON" /><Label value="VV" /><Label value="PU" /><Label value="VC" />"""
    label_Labels=""
    for i in range(n):
        label_Labels = label_Labels+"""<Header size="6" value=\""""+str(i+1)+""":" />""" """<Text name=\"txt-"""+str(i+1)+"""\" value="$text" />"""
        label_Labels = label_Labels+"""<Labels name=\"lbl-"""+str(i+1)+"""\" toName=\"txt-"""+str(i+1)+"""\">"""
        label_Labels = label_Labels+label_tags
        label_Labels = label_Labels+"</Labels>"
    label_choic="""  <Header value="Select The right Dependency:" />
<Choices name="selection" toName="txt-1" required="true" choice="single">"""
    for i in range(n):
        label_choic = label_choic +"<Choice value=\""+str(i+1)+":"+"$text"+"\"/>"
    label_choic = label_choic + "</Choices>"
    
    # <Header value="Select True Dependency Tree" />
    l_c =""" <View>"""+label_choic+label_ralation+label_Labels+"""</View>"""
    project = ls.start_project(
        title='Adonis',
        label_config=l_c
    )
    #convert to dic
    #{'ids':i,'sen': sen[i].sen,'im':dic[sen[i].sen]},
    se = set()
    project.import_tasks("dependency_tree\\zuixin.json")
   
if __name__ == '__main__':
   
    with open('dependency_tree\\config.json','r',encoding='gbk')as fp:
            config=json.load(fp)
    print(config)
    LABEL_STUDIO_URL = config['LABEL_STUDIO_URL']
    #API_KEY = '72deb692101d5d12d3388a76580c10b730e864b0'
    API_KEY = config['API_KEY']
    file_path = config['file_path']
    fila_name = config['fila_name']
    out_path = config['out_path']
    num = config['n']
    dataset = []
    data = model.Conll_8best_Read(dataset)
    dataset = data.read_mul_file(file_path,fila_name)
    sen = tools.load_data_conll(dataset)
    se,dic = tools.find_sent(sen)
    # os.popen("conda activate pytorch")
    # #os.system("label-studio start")
    # s=os.popen("label-studio start")
    #tasks = tools.generate_DPtree_spacy(sen,dic,out_path)
    tasks = tools.generate_DPtree_ls(sen,dic,out_path)
    ls = ServerLaunch(LABEL_STUDIO_URL,API_KEY)
    create_proj(ls,sen,tasks,num)

    