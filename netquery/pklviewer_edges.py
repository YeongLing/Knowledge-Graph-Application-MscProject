import pandas as pd
import pickle

#输入要查看的文件名称
obj=pd.read_pickle(r'..\\engineering_data\\train_edges.pkl')
reldict={}

for edge in obj:
    type,rel=edge[0][0],edge[0][1][1]
    anchor_node,target_node,relation=rel[2],rel[0],rel[1]
    if relation!='0':
        rel = anchor_node + '->' + relation + '->' + target_node
        if rel not in reldict:
            reldict[rel]=1
        else:
            reldict[rel]+=1
reldict=sorted(reldict.items(),key=lambda x:x[1],reverse=True)

#输入要保存的文件名称
with open('..\\engineering_data\\train_edges.txt','w') as file:
    file.write('The relation between nodes:'+'\n')
    for i in reldict:
        file.write(str(i)+'\n')

