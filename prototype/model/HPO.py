import sys
from collections import defaultdict
sys.path.append(".")

import config.config as config
import utils.IOUtils as IOUtils

# Note: HPO Node means a HPO object, while HPO Term means a string like HP:xxxxxxx

class HPO:
    def __init__(self) -> None:
        self.id = None
        self.name = None
        self.parents = set()      # parent is a set of term id
        self.children = set()     # children is a set of term id
        self.alternates = set()   # alternates is a set of term id replaced by this term
        self.ancestors = set()    # ancestors is a set of term id, which includes parents, grandparents, etc.
        self.descendants = set()  # descendants is a set of term id, which includes children, grandchildren, etc.
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
    
    def addHPO(self, HPONode):
        if (len(HPONode.parents) == 0 and HPONode.id != 'HP:0000001'):
            self.noParentNodes.add(HPONode)
        else:
            if (HPONode.id == 'HP:0000001'):
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
    
    def setIC(self, HPOIC):
        self.IC = HPOIC

    def getSimilarity(self, term1, term2):
        """
        Lin measure, see Lin D. An information-theoretic definition of
        similarity. In: ICML, vol. Vol. 98, no. 1998; 1998. p. 296-304.
        """
        if (term1 == term2):
            return 1
        else:
            node1 = self.HPOList[term1]
            node2 = self.HPOList[term2]
            ICTerm1 = self.IC[term1]
            ICTerm2 = self.IC[term2]
            commonAncestors = list(node1.getGeneralAncestors() & node2.getGeneralAncestors())
            if (len(commonAncestors) == 0):
                print("?")
            IC_MICA = max([self.IC[ancestor] for ancestor in commonAncestors])
            if (ICTerm1 + ICTerm2 == 0):
                similarity = 0
            else:
                similarity = 2 * IC_MICA / (ICTerm1 + ICTerm2)
            return similarity


    # handle tempReplaceMap for 'replaced_by' term
    # handle no parent nodes if they are replaced by others
    def replace(self):
        for (oldTerm, newTerm) in self.tempReplaceMap:
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
    def relink(self):
        for (term, node) in self.HPOList.items():
            for parent in node.parents:
                if (self.HPOList.get(parent) == None):
                    IOUtils.showInfo(f"Cannot find term {parent}, which is a parent of term {term}", 'ERROR')
                else:
                    self.HPOList[parent].addChild(node.id)
        
        # for (term, node) in self.HPOList.items():
        #     node.descendants |= node.children
        
        self.relinkNode(set(), self.rootNode)
        # if (self.iterate):
        #     self.relinkNode(set(), self.rootNode)
        # else:
        #     self.relinkAll()

    # get current node. The input term may be current, or may be replaced
    def getHPO(self, termID):
        # todo: in replace map
        validHPO = self.HPOList.get(termID)
        if (validHPO != None):
            result = validHPO
        else:   # no valid HPO available. Need to search in replacement
            result = self.replaceMap.get(termID)
            IOUtils.showInfo('Term {termID} is replaced by {result.id}', 'WARN')
        return result

    # get current term. The input term may be current, or may be replaced
    def getValidHPOTerm(self, termID):
        if (self.HPOList.get(termID) != None):
            result = termID
        else:
            result = self.replaceMap.get(termID).id
            IOUtils.showInfo('Term {termID} is replaced by {result}', 'WARN')
        return result

    def getValidHPOTermList(self):
        return list(self.HPOList.keys())
    
    # calculate ancestors and descendants recursively, which costs 0.3s
    def relinkNode(self, ancestorList, node):  # ancestorList is the path of terms from root to currentNode
        node.ancestors |= ancestorList
        thisset = set()
        thisset.add(node.id)
        newAncestorList = ancestorList | thisset
        for childTerm in node.children:
            descendantList = self.relinkNode(newAncestorList, self.HPOList[childTerm])
            node.descendants |= descendantList
        return node.descendants

    # Another version to calculate ancestors and descendants, which costs 0.7s
    # def relinkAll(self):
    #     modified = True
    #     while (modified):
    #         modified = False
    #         for (term, node) in self.HPOList.items():
    #             for parentTerm in node.parents:
    #                 parentNode = self.HPOList[parentTerm]
    #                 originLength = len(parentNode.descendants)
    #                 parentNode.descendants |= node.descendants
    #                 newLength = len(parentNode.descendants)
    #                 modified |= (originLength != newLength)
    #             for childTerm in node.children:
    #                 childNode = self.HPOList[childTerm]
    #                 originLength = len(childNode.ancestors)
    #                 childNode.ancestors |= node.ancestors
    #                 newLength = len(childNode.ancestors)
    #                 modified |= (originLength != newLength)
