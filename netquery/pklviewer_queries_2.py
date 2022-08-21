import pandas as pd
import pickle

#输入要查看的文件名称
obj=pd.read_pickle(r'..\\engineering_data\\val_queries_2.pkl')
rel_type=[]
rels={}
for edge in obj:
    type,rel1,rel2=edge[0][0],edge[0][1][1],edge[0][2][1]
    if type not in rel_type:
        rel_type.append(type)
    if not (rel1[1]=='0' and rel2[1]=='0'):
        rel=((rel1[0]+'->'+rel1[1]+'->'+rel1[2]),(rel2[0]+'->'+rel2[1]+'->'+rel2[2]))
        rels[rel]=rels.get(rel,0)+1
rels=sorted(rels.items(),key=lambda x: x[1],reverse=True)
#输入要保存的文件名称
with open('..\\engineering_data\\val_queries_2.txt','w') as file:
    file.write('The relation types in val_queries_2.pkl:\n')
    file.write(str(rel_type)+'\n')
    file.write('The inter queries:\n')
    for i in range(len(rels)):
        file.write(str(rels[i])+'\n')

