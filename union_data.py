import re
import pandas as pd

'''
合并人工筛选后的语料(由data_process.py产生)和conver_format.py 产生的标准文件，输出question和index。
'''

#人工筛选的语料文件
file_small = 'test.txt'
#标准文件
file_big = 'test.csv'
#读取的列
column_q = 'question'
column_i = 'index'
#输出文件
out_file = 'mytest.csv'

#读数据
f = open(file_small,"r", encoding='utf-8')
line = f.readline()
data = pd.read_csv(file_big, encoding='utf-8')
out_data_q = data[column_q].tolist()
out_data_i = data[column_i].tolist()

base_l = []
cmp_l = []
while line :
    #读取基准问句和相似问句
    basestr = re.findall(".*base:(.*), cmp:.*", line, re.M)[0]
    cmpstr = re.findall(".*, cmp:(.*), score is:.*", line, re.M)[0]

    #插入挖掘到的相似问句
    flag = 0
    for i in range(len(out_data_q)):
        if basestr == out_data_q[i] :
            out_data_q.insert(i+1, cmpstr)
            out_data_i.insert(i+1, out_data_i[i])
            flag = 1

    #输出没找到的文件
    if flag == 0 :
        print("not find base:", basestr," cmp:", cmpstr)

    line = f.readline()

#存储
dataframe = pd.DataFrame({'question':out_data_q, 'index': out_data_i})
dataframe.to_csv(out_file, index=False, encoding='utf-8')
