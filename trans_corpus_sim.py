import pandas as pd
import random

'''
根据文档，生成 pair-wise语料集，提供匹配模型训练使用
pos pos 1
pos neg 0
'''

#配置和读取数据

#输入文件
in_file = 'translate_data.csv'
#输出文件
out_file = 'trans.csv'
#读取列
column_q = 'question'
column_i = 'index'
#正负向本对数量，建议正负比为1:3
pos_num =  20
neg_num = 3*pos_num

data = pd.read_csv(in_file, encoding='utf-8')

out_data_q = data[column_q]
out_data_i = data[column_i]

#获取每个类的位置分布
index_l = [0]
data_len = len(out_data_i)
for i in range (1, data_len):
    if out_data_i[i-1] != out_data_i[i] :
        index_l.append(i-1)
        index_l.append(i)

index_l.append(data_len-1)

#获取随机的pair
index_len = len(index_l)
trans_l = []
trans_reverse = []
for j in range (0, index_len, 2):
    min = index_l[j]
    max = index_l[j+1]

    #获取正pair
    count = pos_num
    while 1:
        if count == 0:
            break
        pos_a = random.randint(min, max)
        pos_b = random.randint(min, max)
        if pos_a == pos_b:
            continue
        pos_str = out_data_q[pos_a] + ',' + out_data_q[pos_b] + ',' + '1'
        trans_l.append(pos_str)
        pos_str = out_data_q[pos_b] + ',' + out_data_q[pos_a] + ',' + '1'
        trans_reverse.append(pos_str)
        count = count - 1

    #获取负pair
    count = neg_num
    while 1:
        if count == 0:
            break
        pos_index = random.randint(min, max)
        neg_index = random.randint(0, data_len-1)

        if neg_index >= min and neg_index <= max :
            continue
        neg_str = out_data_q[pos_index]+','+out_data_q[neg_index]+','+'0'
        trans_l.append(neg_str)
        neg_str = out_data_q[neg_index] + ',' + out_data_q[pos_index] + ',' + '0'
        trans_reverse.append(neg_str)
        count = count - 1

#打散队列

forward = set(trans_l)
reverse = set(trans_reverse)
same = list(forward & reverse)
forward_l = list(forward)


while len(same) != 0 :
    forward_l.remove(same[0])
    line = same[0].split(',')
    if line[1]+','+line[0]+','+line[2] in same:
        same.remove(line[1]+','+line[0]+','+line[2])
    same.remove(same[0])

random.shuffle(forward_l)
dataframe = pd.DataFrame(forward_l)
dataframe.to_csv(out_file, index=False, encoding='utf-8')

