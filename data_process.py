import pandas as pd
import re
from bert_serving.client import BertClient
import numpy as np
import gensim
from pyhanlp import *
#import jieba

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
    # 输出的向量文件
    file_out = "yuliao_word.npy"
    file_out2 = "zhishidian_word.npy"
    # 向量生产方法
    #vec_type = "bert"
    vec_type = "word"
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
                if len(cq) != 0 and cq not in question_list:
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


"""获取bert的向量"""
def bert_vec(bc, sentence):
    return bc.encode([sentence])

"""获取word2vec的向量"""
def word_vec(model, sentence):
    words = HanLP.segment(sentence)
    #words = jieba.lcut(sentence)
    #去停用词
    CoreStopWordDictionary = JClass("com.hankcs.hanlp.dictionary.stopword.CoreStopWordDictionary")
    CoreStopWordDictionary.apply(words)
    HanLP.Config.ShowTermNature = False

    v = np.zeros(64)
    for word in words :
        v += model[str(word)]
    v /= len(words)
    return v

'''获取向量表示'''
def get_vec(question_list, prcess_conifg):
    question_vec = []

    if prcess_conifg.vec_type == "bert" :
        bc = BertClient(ip="127.0.0.1")
        for question in question_list:
            question_vec.append(bert_vec(bc, question)[0])
        bc.close()

    if prcess_conifg.vec_type == "word" :
        model_file = '/data/dataset/news_12g_baidubaike_20g_novel_90g_embedding_64.bin'
        model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=True)
        print("load 模型完成")
        for question in question_list:
            #去除英文、数字和其他字符，可以选择不要
            r_s = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
            question_t = re.sub(r_s, '', question)
            question_vec.append(word_vec(model, question_t))

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
    emb = np.array([base_vec, cmp_vec])
    return  cosine(emb[0], emb[1])


def main():
# 1. 配置参数
    myconifg = PrcessConifg()

# 2. 编写需要的执行的函数
#    pipeline = ["xlsx_to_csv", "data_extract"]

    pipeline = {"a":1, "b":1, "c": 1, "d": 0}


# 3. 获取向量
    if pipeline["a"] == 1 :
        print("获取语料-cmp")
        get_class("xlsx_to_csv")(myconifg)
        cmp_list =  get_class("data_extract")(myconifg)


    if pipeline["b"] == 1:
        print("获取语料-base")
        myconifg.file_dest="zhishidian.csv"
        myconifg.column="知识标题"
        myconifg.column2="相似问法"
        myconifg.extract_type="zhishidian"

        get_class("xlsx_to_csv")(myconifg)
        base_list = get_class("data_extract")(myconifg)


# 4. 存储向量文件
    if pipeline["c"] == 1:
        print("获取向量")
        cmp_vector = get_vec(cmp_list, myconifg)
        base_vector = get_vec(base_list, myconifg)

        np.save(myconifg.file_out, cmp_vector)
        np.save(myconifg.file_out2, base_vector)

# 5. 计算相似度
    if pipeline["d"] == 1:

        cmp_vec = np.load(myconifg.file_out)
        base_vec = np.load(myconifg.file_out2)

        print("计算相似度")
        len_base_vec = len(base_vec)
        len_cmp_vec = len(cmp_vec)

        print("base vec 的长度是: %d \n" % (len_base_vec))
        print("cmp vec 的长度是: %d \n" % (len_cmp_vec))
        print("总共需要计算的次数: %d \n" % ( len_base_vec * len_cmp_vec ))

        count = 0
        similar = 0.8
        print("相似度大于 %3f 结果是：\n" % (similar))
        for i in range(0 ,len_base_vec) :
            for j in range(0, len_cmp_vec):
                sim = similarity(base_vec[i], cmp_vec[j])
                if sim > similar :
                    count = count + 1
                    print("base:%s, cmp:%s , score is: %3f" % (base_list[i], cmp_list[j], sim))

        print("找到相似句子：", count)

if __name__ == '__main__':
    main()


