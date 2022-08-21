import json
from py2neo import Node
from collections import defaultdict

# Node is a class from the library py2Neo
# A Node has a 'label' as the first argument, which will be defined as the 'nodetype'
# A node takes a dictionary(key-value pairs) to store properties

class myNodes:
    def __init__(self):
        self.Node_dict={}
        self.created={}

    def addnode(self,node):
        if node.label not in self.Node_dict:
            self.Node_dict[node.label]=[node]
            self.created[node.label]=[node.nodeproperties['id']]
        elif node.nodeproperties['id'] not in self.Node_dict[node.label]:
            self.Node_dict[node.label].append(node)
            self.created[node.label].append(node.nodeproperties['id'])
        else:
            return

    def get_subclasses(self):
        result=[]
        for k in self.Node_dict.keys():
            result.append(k)
        return result

    def get_subnodes(self,subclass):
        if subclass.label not in self.Node_dict:
            return
        else:
            return self.Node_dict[subclass.label]

class Designer(Node):
    identified_by='id'
    label='designer'
    def __init__(self,number):
        self.nodeproperties={}
        self.nodeproperties['id']=number
        super().__init__(self.label,**self.nodeproperties)

class System(Node):
    identified_by='id'
    label='system'
    def __init__(self,number):
        self.nodeproperties={}
        self.nodeproperties['id']=number
        super().__init__(self.label,**self.nodeproperties)

class Component(Node):
    identified_by='id'
    label='component'
    def __init__(self,number):
        self.nodeproperties={}
        self.nodeproperties['id']=number
        super().__init__(self.label,**self.nodeproperties)

class Supplier(Node):
    identified_by='id'
    label='supplier'
    def __init__(self,number):
        self.nodeproperties={}
        self.nodeproperties['id']=number
        super().__init__(self.label,**self.nodeproperties)

class Function(Node):
    identified_by='id'
    label='function'
    def __init__(self,number):
        self.nodeproperties={}
        self.nodeproperties['id']=number
        super().__init__(self.label,**self.nodeproperties)



