from translate import Py4Js,translate
import pandas as pd
from tqdm import trange
import time

in_file = 'mytest.csv'
out_file = 'translate_data.csv'
column_q = 'question'
column_i = 'index'

data = pd.read_csv(in_file, encoding='utf-8')
out_data_q = data[column_q].tolist()
out_data_i = data[column_i].tolist()

length_data = len(out_data_q)
js=Py4Js()

trans_q = []
trans_i = []
for i in trange(length_data) :
    trans_q.append(out_data_q[i])
    trans_i.append(out_data_i[i])
    eng = translate(js,out_data_q[i],'c2e')
    if eng =='':
        print(i)
        continue
    time.sleep(1)
    chi = translate(js,eng,'e2c')
    if chi =='':
        print(i)
        continue

    if chi != out_data_q[i] :
        trans_q.append(chi)
        trans_i.append(out_data_i[i])

dataframe = pd.DataFrame({'question':trans_q, 'index': trans_i})
dataframe.drop_duplicates().to_csv(out_file, index=False, encoding='utf-8')
