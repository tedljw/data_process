import pandas as pd

import re

'''
read_file = ''

column_q = ''
column_q_s = ''
column_a = ''
'''
read_file = 'yuliao.xlsx'
out_file = 'yuliao.csv'
column_q = '关联问题'
column_q_s = '相似问法'
column_a = '默认'
end_file = 'qa.csv'

'''
data_xls = pd.read_excel(read_file, encoding='utf-8')
data_xls.to_csv(out_file, encoding='utf-8')
'''
data = pd.read_csv(out_file, encoding='utf-8')

out_data = data[column_q]
out_data2 = data[column_q_s]
out_data3 = data[column_a]
length_data = len(out_data)

question_list = []
answer_list = []
index_list = []

for i in range(0,length_data) :

    question_list.append(out_data[i])

    row = out_data3[i]
    answer = row.replace('\r','').replace('\n','').replace('\t','').replace('<p>','')\
        .replace('<br />','').replace('</p>','').replace('<div id="se-knowledge">', '').replace('</div>','')

    answer_list.append(answer)

    index_list.append(i)

    if type(out_data2[i]) == float :
        continue

    questions = re.findall(".*.", out_data2[i], re.M)
    for q in questions:
        question_list.append(q)
        answer_list.append(''.join(answer))
        index_list.append(i)

#save

dataframe = pd.DataFrame({ 'question': question_list, 'answer': answer_list, 'index': index_list})

dataframe.to_csv(end_file, index=False, sep=',', encoding='utf-8')

a=set(index_list)
for i in a:
    count =index_list.count(i)
    if count < 5 :
        print(i,'出现的次数：',count)


