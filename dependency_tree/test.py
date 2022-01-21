#E:\\py基础\\nlp_快速进入研究生状态\\dependency_tree\\output_image\\1364.svg
import cairosvg
import requests
import json
def trans2svg():
    svg_path = 'dependency_tree\\output_image\\1364.svg'
    png_path = 'dependency_tree\\output_image\\1364.png'
    cairosvg.svg2png(url=svg_path, write_to=png_path)

def upload(path):
    url = 'https://sm.ms/api/v2/upload'
    file_obj = open(path,'rb')
    file = {'smfile': file_obj}  # 参数名称必须为smfile
    data_result = requests.post(url, data=None, files=file)
    print(type(data_result.json()))
    print(data_result.json())  # 得到json结果
    a= data_result.json()
    #print(a)
    if a['success'] == False:
        return a['images']
    else:
        return a['data']['url']

upload("300.JPG")