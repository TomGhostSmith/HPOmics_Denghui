import sys
from collections import defaultdict
import numpy
sys.path.append(".")

from config import config
import utils.IOUtils as IOUtils

# Note: HPO Node means a HPO object, while HPO Term means a string like HP:xxxxxxx

class HPO:
    def __init__(self) -> None:
        self.id = None              # e.g. HP:xxxxxxx
        self.name = None            # e.g. headache
        self.index = 0              # index is a number indicating its position in array
        self.parents = set()        # parent is a set of term id, which do not include itself
        self.children = set()       # children is a set of term id, which do not include itself
        self.alternates = set()     # alternates is a set of term id replaced by this term
        self.ancestors = set()      # ancestors is a set of term id, which includes parents, grandparents, etc.
        self.descendants = set()    # descendants is a set of term id, which includes children, grandchildren, etc.
        self.ancestorIndexs = set()   # ancestor indexes, include itself
        # self.ancestorMask = None    # an array full of 0 and 1. 1 means this index of HPO is the ancestor. include itself
        # self.descendantMask = None  # an array full of 0 and 1. 1 means this index of HPO is the descendant. include itself
        self.info = {}

    def setId(self, id):
        self.id = id

    def setName(self, name):
        self.name = name
    
    def addParent(self, parent):
        self.parents.add(parent)
    
    def addAlternate(self, alternate):
        self.alternates.add(alternate)
    
    def addChild(self, child):
        self.children.add(child)
    
    def setInfo(self, key, value):
        self.info[key] = value
    
    def getInfo(self, key):
        return self.info.get(key)

    # get ancestor of this node, including this node itself
    def getGeneralAncestors(self):
        # use union operation to generate a new object, instead of modify the original object
        result = self.ancestors | set()
        result.add(self.id)
        return result

    def getType(self):
        ancestors = self.ancestors
        HPOTypes = set()
        for (key, value) in config.HPOClasses.items():
            if (key in ancestors):
                HPOTypes.add(value)
        return HPOTypes
    
    # test for multiple construction function
    # @classmethod
    # def noName(cls):
    #     return cls(None)
    
class HPOTree:
    def __init__(self) -> None:
        self.rootNode = None
        self.HPOList = dict()         # key is the term, value is the node
        self.tempReplaceMap = dict()  # key is the old term, value is the new term
        self.replaceMap = dict()      # key is the old version HPO Term, value is the new version HPO Node
        self.considerMap = dict()
        self.noParentNodes = set()
        self.IC = None
        self.ICList = None
        self.nonPhenotypicTerms = set()
        self.similarityMatrix = dict()
    
    def addHPO(self, HPONode):
        if (len(HPONode.parents) == 0 and HPONode.id != config.HPORoot):
            self.noParentNodes.add(HPONode)
        else:
            HPONode.index = len(self.HPOList.keys())
            if (HPONode.id == config.HPORoot):
                self.rootNode = HPONode
            self.HPOList[HPONode.id] = HPONode
            for alternate in HPONode.alternates:
                if (self.replaceMap.get(alternate) == None):
                    self.replaceMap[alternate] = HPONode
                else:
                    IOUtils.showInfo(f"HPO term {alternate} is replaced by multiple term", 'WARN')

    def addConsideration(self, oldTerm, newTerm):
        if (self.considerMap.get(oldTerm) == None):
            self.considerMap[oldTerm] = set()
        self.considerMap[oldTerm].add(newTerm)
    
    # WARN: HPOIC.values() remains the original order of HPO. This feature requires python 3.7 or later
    def setIC(self, HPOIC):
        self.IC = HPOIC
        self.ICList = list(HPOIC.values())
    
    def getSimilarity(self, node1, node2, similarityMethod='Lin'):
        if (similarityMethod not in self.similarityMatrix.keys()):
            IOUtils.showInfo('Invalid similarity algorithm', 'ERROR')
        else:
            matrix = self.similarityMatrix.get(similarityMethod)
            if (node1.index == node2.index):
                res = 1
            elif (node1.index < node2.index):
                res = matrix[node2.index, node1.index]
            else:
                res = matrix[node1.index, node2.index]
            return res
            if (numpy.isinf(res) or numpy.isnan(res)):
                IOUtils.showInfo('similarity is not a number', 'ERROR')
                return 0
            else:
                return res

    
    def postProcess(self):
        self.calculateReplacement()
        self.calculateLink()
        self.calculateNonPhenotypicNodes()

    # pick out HPO terms for non phenotypic use (e.g. frequency, blood group, inheritance mode)
    def calculateNonPhenotypicNodes(self):
        for (term, description) in config.specialHPO.items():
            if (description != 'Phenotypic abnormality'):
                specialNode = self.HPOList.get(term)
                if (specialNode != None):
                    self.nonPhenotypicTerms.add(term)
                    for descendant in specialNode.descendants:
                        self.nonPhenotypicTerms.add(descendant)

    # handle tempReplaceMap for 'replaced_by' term
    # handle no parent nodes if they are replaced by others
    def calculateReplacement(self):
        for (oldTerm, newTerm) in self.tempReplaceMap.items():
            newNode = self.HPOList[newTerm]
            if (newNode == None):
                IOUtils.showInfo("Cannot find replacement term {newTerm}", 'ERROR')
            elif (self.replaceMap.get(oldTerm) == None):
                self.replaceMap[oldTerm] = newNode
            elif (self.replaceMap[oldTerm] != newNode):
                IOUtils.showInfo(f"HPO term {oldTerm} is replaced by multiple term", 'WARN')
        
        for node in self.noParentNodes:
            if (self.replaceMap.get(node.id) == None):
                self.HPOList[node.id] = node
                # for alternate in node.alternates:
                #     if (self.replaceMap.get(alternate) == None):
                #         self.replaceMap[alternate] = node
                #     else:
                #         IOUtils.showInfo(f"HPO term {alternate} is replaced by multiple term", 'WARN')
                IOUtils.showInfo(f"Term {node.id} has no parent!", 'ERROR')

    # calc children for each term with 'is_a' information 
    def calculateLink(self):
        for (term, node) in self.HPOList.items():
            # node.ancestorMask = [0] * HPOCount
            node.ancestorIndexs.add(node.index)
            for parent in node.parents:
                if (self.HPOList.get(parent) == None):
                    IOUtils.showInfo(f"Cannot find term {parent}, which is a parent of term {term}", 'ERROR')
                else:
                    self.HPOList[parent].addChild(node.id)
        
        self.relinkNode(set(), set(), self.rootNode)

    # calculate ancestors and descendants recursively, which costs 0.3s
    # arg ancestorList is the path of terms from root to currentNode
    # arg ancestorIndexList is the indexes for ancestorList. Use this arg to boost operation
    def relinkNode(self, ancestorList, ancestorIndexList, node):  
        node.ancestors |= ancestorList
        node.ancestorIndexs |= ancestorIndexList
        thisset = set()
        thisset.add(node.id)
        newAncestorList = ancestorList | thisset
        thisIndexset = set()
        thisIndexset.add(node.index)
        newAncestorIndexList = ancestorIndexList | thisIndexset
        for childTerm in node.children:
            descendantList = self.relinkNode(newAncestorList, newAncestorIndexList, self.HPOList[childTerm])
            node.descendants |= descendantList
        return node.descendants | thisset

    # get current node. The input term may be current, or may be replaced
    def getHPO(self, termID):
        # todo: in replace map
        validHPO = self.HPOList.get(termID)
        if (validHPO != None):
            result = validHPO
        else:   # no valid HPO available. Need to search in replacement
            result = self.replaceMap.get(termID)
            if (result != None):
                IOUtils.showInfo(f'Term {termID} is replaced by {result.id}', 'WARN')
            else:
                IOUtils.showInfo(f'Term {termID} is not valid in HPO version {config.HPOVersion}', 'WARN')
        return result

    # get current term. The input term may be current, or may be replaced
    def getValidHPOTerm(self, termID):
        if (self.HPOList.get(termID) != None):
            result = termID
        else:
            validNode = self.replaceMap.get(termID)
            if (validNode != None):
                result = validNode.id
                IOUtils.showInfo(f'Term {termID} is replaced by {result}', 'WARN')
            else:
                result = None
                IOUtils.showInfo(f'Term {termID} is not valid in HPO version {config.HPOVersion}', 'WARN')
        return result

    def getValidHPOTermList(self):
        return list(self.HPOList.keys())
    
