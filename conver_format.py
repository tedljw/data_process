import pandas as pd

import re
'''
将excel文档的内容转化为 question, answer, index 的形式
'''

'''
read_file = ''

column_q = ''
column_q_s = ''
column_a = ''
'''
#读文件
read_file = 'yuliao.xlsx'
#中间文件
out_file = 'yuliao.csv'
#读取列
column_q = '关联问题'
column_q_s = '相似问法'
column_a = '默认'
#输出文件
end_file = 'qa.csv'

'''
data_xls = pd.read_excel(read_file, encoding='utf-8')
data_xls.to_csv(out_file, encoding='utf-8')
'''
#读数据
data = pd.read_csv(out_file, encoding='utf-8')
out_data_q = data[column_q]
out_data_q_s = data[column_q_s]
out_data_a = data[column_a]
length_data = len(out_data_q)

question_list = []
answer_list = []
index_list = []
for i in range(0,length_data) :
    #存问题
    question_list.append(out_data_q[i])
    #存答案
    row = out_data_a[i]
    answer = row.replace('\r','').replace('\n','').replace('\t','').replace('<p>','')\
        .replace('<br />','').replace('</p>','').replace('<div id="se-knowledge">', '').replace('</div>','')\
        .replace('<span>','').replace('<p style="text-align:left;">', '').replace("</a>", '').replace('<p style="text-align:start;">', '')\
        .replace('<strong>', '').replace('</span>', '').replace('<br>', '').replace('<span style="font-size:12.0px;">', '')
    answer_list.append(answer)
    #存类index
    index_list.append(i)
    #存相似问法
    if type(out_data_q_s[i]) == float :
        continue

    questions = re.findall(".*.", out_data_q_s[i], re.M)
    for q in questions:
        question_list.append(q)
        answer_list.append(''.join(answer))
        index_list.append(i)


#存储
dataframe = pd.DataFrame({ 'question': question_list, 'answer': answer_list, 'index': index_list})
dataframe.to_csv(end_file, index=False, sep=',', encoding='utf-8')

#统计相似问题小于5个的类index
a=set(index_list)
for i in a:
    count =index_list.count(i)
    if count < 5 :
        print(i,'出现的次数：',count)


