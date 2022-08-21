from py2neo import  Node
import pandas as pd

class Relation:
    # Define a relation class, which contains start node, start node type, endnode, endnode type, type of relation, and its property and direction
    def __init__(self,startnodeType,anchornodeType,startNodeID,anchorNodeID,relationtype,bidirection=False,**karq):
        self.startnodeType=startnodeType
        self.anchornodeType=anchornodeType
        self.startnodeID=startNodeID
        self.anchornodeID=anchorNodeID
        self.relationtype=relationtype
        self.bidirection=bidirection

    def getsubClasses(cls):  # get all subclasses of a class
        result = []
        for subclass in cls.__subclass__():
            result.append(subclass)
        return result

    def getRelationLabel(cls):  # get all labels of the relations
        result = [a.label for a in cls.getsubClasses()]
        return result

    def getRelationDict(cls):  # get the {label:class} dictionary of a relation
        dic = {}
        for a in cls.getsubClasses():
            dic[a.label] = a
        return dic

    # get the equivalence(synonym) dictionary for relations
    def getEquivalenceDict(cls):
        dic = {}
        for a in cls.getsubClasses():
            for b in a.equivalence:
                if b in dic:
                    dic[b].append(a.label)
                else:
                    dic[b] = [a.label]
        return dic

    def getInverseDict(cls):  # get the inverse(antonym) dictionary for relations
        dic = {}
        for a in cls.getsubClasses():
            for b in a.inverse:
                if b in dic:
                    dic[b].append(a.label)
                else:
                    dic[b] = [a.label]
        return dic

    def __str__(self):
        if self.bidirection == False:
            return(f"Relation(({self.startnodeType}:{self.startnodeID})-({self.relationType}:{self.property})->({self.endnodeType}:{self.endnodeID})")
        else:
            return(f"Relation(({self.startnodeType}:{self.startnodeID})-({self.relationType}:{self.property})-({self.endnodeType}:{self.endnodeID})")

    def __repr__(self):
        if self.bidirection == False:
            return(f"Relation(({self.startnodeType}:{self.startnodeID})-({self.relationType}:{self.property})->({self.endnodeType}:{self.endnodeID})")
        else:
            return(f"Relation(({self.startnodeType}:{self.startnodeID})-({self.relationType}:{self.property})-({self.endnodeType}:{self.endnodeID})")

class fromDesignertoSupplier(Relation):
    label='works_in'
    startnodeType='Designer'
    anchornodeType='Supplier'
    inverse=['employs']
    def __init__(self,Designer,Supplier):
        super().__init__(self.startnodeType,self.anchornodeType,Designer,Supplier,self.label)

class fromDesignertoComponent(Relation):
    label='designs'
    startnodeType='Designer'
    anchornodeType='Component'
    inverse=['is_designed_by']
    def __init__(self,Designer,Component):
        super(fromDesignertoComponent, self).__init__()
        #super().__init__(self.startnodeType,self.anchornodeType,Designer,Component,self.label)

class fromComponenttoSystem(Relation):
    label='belongs_to'
    startnodeType='Component'
    anchornodeType='System'
    inverse=['has']
    def __init__(self,Component,System):
        super().__init__(self.startnodeType,self.anchornodeType,Component,System,self.label)

class innerinteract_Designer(Relation):
    label='is_collegue_of'
    startnodeType='Designer'
    anchornodeType='Designer'
    inverse=['is_collegue_of']
    def __init__(self,Designer_a,Designer_b):
        super().__init__(self.startnodeType,self.anchornodeType,Designer_a,Designer_b,self.label)

class innerinteract_system(Relation):
    label='belongs_to_the_same_department_with'
    startnodeType='System'
    anchornodeType='System'
    inverse=['in_the_same_department']
    def __init__(self,System_a,System_b):
        super().__init__(self.startnodeType,self.anchornodeType,System_a,System_b,self.label)
