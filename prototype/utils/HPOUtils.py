import os
import datetime
import sys
import json
sys.path.append(".")

import config.config as config
import utils.IOUtils as IOUtils
from model.HPO import HPO
from model.HPO import HPOTree
from model.Disease import Disease
from model.Gene import Gene
def loadHPOTree():
    tree = HPOTree()
    currentNode = None
    currentTerm = None
    with open(file=config.HPOTermFilePath, mode='rt', encoding='utf-8') as fp:
        for line in fp:
            line = line.strip()

            if (line.startswith('[Typedef]')):
                # submit the former node if there is already a node recorded
                if (currentNode != None):
                    tree.addHPO(currentNode)
                
                # term start with '[Typedef]' will not be recorded
                currentNode = None
                currentTerm = None
            elif (line.startswith('[Term]')):
                # submit the former node if there is already a node recorded
                if (currentNode != None):
                    tree.addHPO(currentNode)

                currentNode = HPO()
                currentTerm = None
            elif (line.startswith('id') and currentNode != None):
                currentTerm = line[4:]
                currentNode.setId(currentTerm)
            elif (line.startswith('name') and currentNode != None):
                currentNode.setName(line[6:])
            elif (line.startswith('alt_id') and currentNode != None):
                currentNode.addAlternate(line[8:])
            elif (line.startswith('is_a') and currentNode != None):
                term = line[6:]   # term contains id and name
                currentNode.addParent(term.split('!')[0].strip())   # only use id in the parent list
            elif (line.startswith('replaced_by')):
                newTerm = line[13:]
                tree.tempReplaceMap[currentTerm] = newTerm
                currentNode = None
            elif (line.startswith('consider')):
                newTerm = line[10:]
                tree.addConsideration(oldTerm=currentTerm, newTerm=newTerm)
                currentNode = None

    # submit the former node if there is already a node recorded
    if (currentNode != None):
        tree.addHPO(currentNode)

    # calc children for each term with 'is_a' information 
    tree.relink()

    return tree

# IOUtils.showInfo("Start loading HPO tree")
# a = loadHPOTree()
# IOUtils.showInfo("Loaded with iterate")
# b = loadHPOTree()
# IOUtils.showInfo("Loaded without iterate")
# hpos = list(a.HPOList.keys())
# for hpo in hpos:
#     an = a.HPOList[hpo]
#     bn = b.HPOList[hpo]
#     if (len(an.ancestors) != len(bn.ancestors)):
#         IOUtils.showInfo(f"Term {hpo} not same!", 'ERROR')
# IOUtils.showInfo("release iterated result")
# a = None
# IOUtils.showInfo("release non-iterated result")
# b = None
# IOUtils.showInfo("Done")