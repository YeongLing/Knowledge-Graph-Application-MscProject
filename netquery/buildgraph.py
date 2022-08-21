from argparse import ArgumentParser
from py2neo import  Graph,Node,NodeMatcher
from netquery.graphparser import parseinfo
from netquery.nodetypes import myNodes,Designer,System,Component,Supplier,Function

class Buildgraph:
    def __init__(self):
        print('Connecting Neo4j...')
        # Connect to the Neo4j database
        self.g = Graph("neo4j+s://ebb34a1a.databases.neo4j.io:7687", auth=("neo4j", "L-2KGxJ7dGFGILlWNaKk6xDCoFBVovr80gDdmn6_MqE"))


    def createNodes(self, nodes):
        # A funciotn to create nodes in the Neo4j graph database from the list of nodes
        print('Creating nodes...')
        for v in nodes.Node_dict.values():
            for i in v:
                self.g.create(i)

    def deleteall(self):
        self.g.delete_all()

    def createrelations(self,queries):
        print('Creating relations...')
        for query in queries:
            print(query)
            self.g.run(query)


fpath='../engineering_data/val_edges.pkl'
nodes,queries=parseinfo(fpath)
graph=Buildgraph()
graph.deleteall()
graph.createNodes(nodes)
graph.createrelations(queries)






