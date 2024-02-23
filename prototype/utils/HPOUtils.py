import os
import datetime
import sys
import json
import numpy
sys.path.append(".")

import config.config as config
import utils.IOUtils as IOUtils
from model.HPO import HPO
from model.HPO import HPOTree
from model.Disease import Disease
from model.Disease import DiseaseList
from model.Gene import Gene
from model.Gene import GeneList

if (config.GPUAvailable):
    import cupy
    IOUtils.showInfo("Use GPU to acclerate calculation. Cupy loaded")

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
            elif (line.startswith('is_obsolete: true')):
                currentNode = None

    # submit the former node if there is already a node recorded
    if (currentNode != None):
        tree.addHPO(currentNode)

    tree.postProcess()
    return tree

def loadIC(HPOTree):
    IOUtils.showInfo("Loading IC")
    if (config.ICType == 'disease'):
        with open(file=config.ICFromDiseasePath, mode='rt', encoding='utf-8') as fp:
            HPOTree.setIC(json.load(fp))
    elif (config.ICType == 'gene'):
        with open(file=config.ICFromGenePath, mode='rt', encoding='utf-8') as fp:
            HPOTree.setIC(json.load(fp))
    else:
        with open(file=config.integratedICPath, mode='rt', encoding='utf-8') as fp:
            HPOTree.setIC(json.load(fp))

def loadSimilarity(HPOTree):
    """
    Lin measure, see Lin D. An information-theoretic definition of
    similarity. In: ICML, vol. Vol. 98, no. 1998; 1998. p. 296-304.
    For each pair of term (x, y), sim(x, y) = 2 * MICA(x, y).IC / (x.IC + y.IC)

    Jiang-Conrath measure, see Jiang JJ, Conrath DW. Semantic similarity
    based on corpus statistics and lexical taxonomy. In: Proc of 10th
    international conference on research in computational linguistics,
    ROCLING'97; 1997
    For each pair of term (x, y), sim(x, y) = 1 / (1 + x.IC + y.IC - 2 * MICA(x, y))

    Information coefficient measure, see Li, B., Wang, J. Z., Feltus,
    F. A., Zhou, J., & Luo, F. (2010). Effectively integrating information
    content and structural relationship to improve the GO-based similarity
    measure between proteins. arXiv preprint arXiv: 1001.0958.
    For each pair of term (x, y), sim(x, y) = (2 * MICA(x, y).IC / (x.IC + y.IC)) * (1 / 1 - MICA(x, y))
    """
    IOUtils.showInfo("Loading similarity")
    ICList = HPOTree.ICList
    MICAMatrix = numpy.load(config.MICAMatirxPath)['MICAMatrix']
    if (config.GPUAvailable):
        ICArray = cupy.array(ICList)
        denominatorMatrx = ICArray[:, cupy.newaxis] + ICArray[cupy.newaxis, :]  
        MICAMatrix = cupy.array(MICAMatrix)
        LinSimilarityMatrix = cupy.divide(MICAMatrix * 2, denominatorMatrx)
        JCSimilarityMatrix = cupy.divide(1, 1 + denominatorMatrx - MICAMatrix * 2)
        ICSimilarityMatrix = cupy.multiply(LinSimilarityMatrix, 1 - cupy.divide(1, 1 + MICAMatrix))
        LinSimilarityMatrix = LinSimilarityMatrix.get()
        JCSimilarityMatrix = JCSimilarityMatrix.get()
        ICSimilarityMatrix = ICSimilarityMatrix.get()
    else:
        ICArray = numpy.array(ICList)
        denominatorMatrx = ICArray[:, None] + ICArray[None, :]  
        LinSimilarityMatrix = numpy.divide(MICAMatrix * 2, denominatorMatrx, out=numpy.zeros_like(denominatorMatrx), where=denominatorMatrx != 0)
        JCSimilarityMatrix = numpy.divide(1, 1 + denominatorMatrx - MICAMatrix * 2)
        ICSimilarityMatrix = numpy.multiply(LinSimilarityMatrix, 1 - numpy.divide(1, 1 + MICAMatrix))
    
    # test: make all ancestor-descendant similarity = 1
    # for HPONode in HPOTree.HPOList.values():
    #     thisIndex = HPONode.index
    #     ancestorIndexs = HPONode.ancestorIndexs
    #     for ancestorIndex in ancestorIndexs:
    #         LinSimilarityMatrix[thisIndex, ancestorIndex] *= 1.2
    #         LinSimilarityMatrix[ancestorIndex, thisIndex] *= 1.2
    #         JCSimilarityMatrix[thisIndex, ancestorIndex] *= 1.2
    #         JCSimilarityMatrix[ancestorIndex, thisIndex] *= 1.2
            

    HPOTree.similarityMatrix['Lin'] = LinSimilarityMatrix
    HPOTree.similarityMatrix['JC'] = JCSimilarityMatrix
    HPOTree.similarityMatrix['IC'] = ICSimilarityMatrix
    IOUtils.showInfo("Similarity loaded")

# convert HPO terms to nodes, filter out invalid terms, filter out non-phenotypic terms
# only preserve most precise term (i.e. preserve child node and discard parent node)
def extractPreciseHPONodes(HPOTree, originHPOTerms):
    result = dict()  # key is the node, value is a bool, indicate whether preserve or not
    for term in originHPOTerms:
        validNode = HPOTree.getHPO(term.strip())
        if (validNode != None and validNode.id not in HPOTree.nonPhenotypicTerms):
            shouldPreserve = True
            for (node, preserve) in result.items():
                if (preserve):
                    if (validNode.id in node.ancestors):  # this node is an ancestor of some other node
                        shouldPreserve = False
                    elif (validNode.id in node.descendants): # this node is a descendant of some other node
                        result[node] = False
            result[validNode] = shouldPreserve
    preservedResult = set()
    totalIC = 0
    for (node, preserve) in result.items():
        if (preserve):
            preservedResult.add(node)
            totalIC += HPOTree.ICList[node.index]
    return preservedResult, totalIC

def loadDiseases(HPOTree):
    diseaseList = DiseaseList()
    with open(file=config.disease2PhenotypeJsonPath, mode='rt', encoding='utf-8') as fp:
        disease2PhenotypeJson = json.load(fp)
    for (id, disease) in disease2PhenotypeJson.items():
        relatedHPONodes, totalIC = extractPreciseHPONodes(HPOTree, disease['phenotypeList'])
        diseaseList.addDisease(Disease(id, disease['name'], relatedHPONodes, totalIC))
    return diseaseList

def loadGenes(HPOTree):
    geneList = GeneList()
    with open(file=config.gene2PhenotypeJsonPath, mode='rt', encoding='utf-8') as fp:
        gene2PhenotypeJson = json.load(fp)
    for (id, gene) in gene2PhenotypeJson.items():
        relatedHPONodes, totalIC = extractPreciseHPONodes(HPOTree, gene['phenotypeList'])
        geneList.addGene(Gene(id, gene['name'], relatedHPONodes, totalIC))
    return geneList