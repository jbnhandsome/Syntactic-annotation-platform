import model
import tools
import server

if __name__ == '__main__':
    file_path = "E:/baiduyunxiazai/zx/"
    fila_name = "notMatch.alldata"
    out_path = "dependency_tree/output_image"
    LABEL_STUDIO_URL = 'http://localhost:8080'
    API_KEY = '72deb692101d5d12d3388a76580c10b730e864b0'
    #ls = server.ServerLaunch(LABEL_STUDIO_URL,API_KEY)
    dataset = []
    data = model.Conll_8best_Read(dataset)
    dataset = data.read_mul_file(file_path,fila_name)
    sen = tools.load_data_conll(dataset)
    se,dic = tools.find_sent(sen)
    example = "只不过，在这之后，张小凡也感觉到，从绑在自己右手臂膀上的那个奇异法宝，却似乎散发着与烧火棍相反的，带着一丝温暖的气息，传进自己的身体。"
    tools.generate_DPtree_graphiz(sen,example,dic,out_path)
    tools.generate_DPtree_spacy(sen,example,dic,out_path)
    