import pandas as pd

file = 'mytest.csv'
column_q = 'question'
column_i = 'index'

data = pd.read_csv(file, encoding='utf-8')
out_data_q = data[column_q].tolist()
out_data_i = data[column_i].tolist()

class_set=set(out_data_i)
max = [1, 0]
min = [10, 0]
counter = 0
count_l = []
for c in class_set:
    count =out_data_i.count(c)
    if count > max[0] :
        max[0] = count
        max[1] = c

    if count < min[0]:
        min[0] = count
        min[1] = c

    if count < 4 :
        print("index: ",c ,"出现的次数：",count)
        counter = counter + 1
        count_l.append(c)

print("the max is: ",max[0], "the index is: ", max[1])
print("the min is: ",min[0], "the index is: ", min[1])
print("the low then 4 counter is: ", counter)

for i in count_l:
    for j in range(len(out_data_i)) :
        if i ==  out_data_i[j]:
            tmp = out_data_q[j]+','+str(i)
            print(tmp)