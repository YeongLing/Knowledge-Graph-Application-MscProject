import pandas as pd
import pickle
from py2neo import Node
from netquery.nodetypes import myNodes,Designer,System,Component,Supplier,Function

def parseinfo(fpath):
    obj=pd.read_pickle(fpath)
    n=myNodes()
    queries=[]
    print('Parsing nodes and relations...')
    for edge in obj:
        rel = edge[0][1][1]
        for i in [0,2]:
            node_num,node_type=edge[0][1][i],rel[i]
            if node_type not in n.Node_dict or node_num not in n.created[node_type]:
                if node_type=='function':
                    new_node=Function(node_num)
                elif node_type=='system':
                    new_node=System(node_num)
                elif node_type=='designer':
                    new_node=Designer(node_num)
                elif node_type=='component':
                    new_node=Component(node_num)
                else:
                    new_node=Supplier(node_num)
                #new_node=type(node_type,(Node,),{'label':node_type,'identified_by':'id','nodeproperties':{'id':node_num}})
                n.addnode(new_node)
        if rel[1]!='0':
            anchor_num,target_num=edge[0][1][2],edge[0][1][0]
            anchor_type,target_type=rel[2],rel[0]
            anchor_node,target_node=n.Node_dict[anchor_type][n.created[anchor_type].index(anchor_num)],n.Node_dict[target_type][n.created[target_type].index(target_num)]
            relation=type(rel[1],(object,),{'anchor_type':anchor_type,'anchor_num':anchor_num,'relation_type':rel[1],'target_type':target_type,'target_num':target_num})
            query = f"match(p:{relation.anchor_type}) " +\
                    f"match (q:{relation.target_type}) " +\
                    f"where p.{anchor_node.identified_by} = {anchor_num} and q.{target_node.identified_by} = {target_num} " +\
                    f"merge(p)-[r:{relation.relation_type}] -> (q) "
            queries.append(query)
    return n,queries
