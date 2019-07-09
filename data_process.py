import pandas as pd
import re
from bert_serving.client import BertClient
import numpy as np

"""配置"""
class PrcessConifg(object):
    # 输入文档
    #file_src = "历史会话19到23.xls"
    file_src = ""
    # 输出的csv文档
    file_dest = "yuliao.csv"
    # 需要获取的列
    column = "对话详情"
    column2 = ""
    # 输出的语料文件
    file_out = ""
    # 向量生产方法
    vec_type = "bert"
    # csv数据处理
    extract_type = "yuliao"

"""excel转csv"""
def xlsx_to_csv_pd(prcess_conifg):

    if prcess_conifg.file_src == '':
        return
    data_xls = pd.read_excel(prcess_conifg.file_src, index_col=0)
    data_xls.to_csv(prcess_conifg.file_dest, encoding='utf-8')

"""从csv提取数据"""
def data_extract(prcess_conifg):
    if prcess_conifg.column == '':
        print("column is nill \n")
        return

    question_list = []
    data = pd.read_csv(prcess_conifg.file_dest, encoding='utf-8')

    if prcess_conifg.extract_type == "yuliao":
        out_data = data[prcess_conifg.column].drop_duplicates(keep ='first')
#        for q in out_data.loc[0:2] :
        for q in out_data :
            if type(q) == float :
                continue
        
            result = re.findall(".\d:(.*).\n", q, re.M)
            for cq in result:
                if len(cq) != 0:
                    question_list.append(cq)


    if prcess_conifg.extract_type == "zhishidian":
        out_data = data[prcess_conifg.column]
        out_data2 = data[prcess_conifg.column2]
        length_data =  len(out_data)

#        for i in range(0,3) :
        for i in range(0,length_data) :
            question_list.append(out_data[i])
            if type(out_data2[i]) == float :
                continue

            result = re.findall(".*.", out_data2[i], re.M)
            for cq in result:
                question_list.append(cq)


    return question_list
    #out_data.to_csv(csv_conifg.file_out)


"""获取bert的向量"""
def bert_vec(bc, sentence):
    return bc.encode([sentence])

"""获取word2vec的向量"""
def word_vec(sentence):
    pass

'''获取向量表示'''
def get_vec(question_list, prcess_conifg):
    question_vec = []

    if prcess_conifg.vec_type == "bert" :
        bc = BertClient(ip="127.0.0.1")
        for question in question_list:
            question_vec.append(bert_vec(bc, question))
        bc.close()

    if prcess_conifg.vec_type == "word" :
        for question in question_list:
            question_vec.append(word_vec(question))

    return question_vec

""" 执行函数映射 """
def get_class(task_name):
    processors = {"xlsx_to_csv": xlsx_to_csv_pd, "data_extract": data_extract}
    if task_name not in processors:
        raise ValueError("Task not found: %s" % (task_name))

    return processors[task_name]

def cosine(a, b):
    return a.dot(b) / (np.linalg.norm(a) * np.linalg.norm(b))

"""相似度计算"""
def similarity(base_vec, cmp_vec):
    emb = np.array([base_vec[0], cmp_vec[0]])
    return  cosine(emb[0], emb[1])


def main():
# 1. 配置参数
    myconifg = PrcessConifg()

# 2. 编写需要的执行的函数
#    pipeline = ["xlsx_to_csv", "data_extract"]

    print("获取向量-cmp")
# 3. 获取向量
    get_class("xlsx_to_csv")(myconifg)
    cmp_list =  get_class("data_extract")(myconifg)
    cmp_vec = get_vec(cmp_list, myconifg)


    print("获取向量-base")

    myconifg.file_dest="zhishidian.csv"
    myconifg.column="知识标题"
    myconifg.column2="相似问法"
    myconifg.extract_type="zhishidian"

    get_class("xlsx_to_csv")(myconifg)
    base_list = get_class("data_extract")(myconifg)
    base_vec = get_vec(base_list, myconifg)

# 4. 计算相似度

    print("计算相似度")
    len_base_vec = len(base_vec)
    len_cmp_vec = len(cmp_vec)

    print("base vec 的长度是: %d \n" % (len_base_vec))
    print("cmp vec 的长度是: %d \n" % (len_cmp_vec))
    print("总共需要计算的次数: %d \n" % ( len_base_vec * len_cmp_vec ))

    similar = 0.95
    print("相似度大于 %3f 结果是：\n" % (similar))
    for i in range(0 ,len_base_vec) :
        for j in range(0, len_cmp_vec):
            sim = similarity(base_vec[i], cmp_vec[j])
            if sim > similar :
                print("base:%s, cmp:%s , score is: %3f" % (base_list[i], cmp_list[j], sim))


if __name__ == '__main__':
    main()

