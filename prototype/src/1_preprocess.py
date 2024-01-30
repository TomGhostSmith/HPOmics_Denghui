# program should run under root folder of the project
import sys
import json
import math
import numpy
import cupy
sys.path.append(".")

import config.config as config
import utils.IOUtils as IOUtils
import utils.HPOUtils as HPOUtils
from model.HPO import HPO
from model.HPO import HPOTree
from model.Disease import Disease
from model.Gene import Gene

def calcGene2PhenotypeJson(tree):
    IOUtils.showInfo("Calculating gene to phenotype json.")
    gene2Phenotype = dict()
    with open(file=config.gene2PhenotypeAnnotationPath, mode='rt', encoding='utf-8') as fp:
        fp.readline()  # skip the first line (title line)

        line = fp.readline()
        while (line):
            termsInLine = line.strip().split('\t')
            if (len(termsInLine) >= 3):
                geneId = int(termsInLine[0])
                geneSymbol = termsInLine[1]
                phenotype = termsInLine[2]
                if (gene2Phenotype.get(geneId) == None):
                    gene2Phenotype[geneId] = {
                        "name": set(),
                        "phenotypeList": set()
                    }
                gene2Phenotype[geneId]["name"].add(geneSymbol)
                gene2Phenotype[geneId]["phenotypeList"].add(tree.getValidHPOTerm(phenotype))

            line = fp.readline()

    # check if one id has multiple names, and convert set to list
    for (key, value) in gene2Phenotype.items():
        value["name"] = list(value["name"])
        value["phenotypeList"] = list(value["phenotypeList"])
        if (len(value["name"]) > 1):
            IOUtils.showInfo(f"Gene ID '{key}' has multiple symbols: {value['name']}", 'WARN')
        
    with open(file=config.gene2PhenotypeJsonPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=gene2Phenotype, fp=fp, indent=2, sort_keys=True)

    with open(file=config.geneListPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=list(gene2Phenotype.keys()), fp=fp, indent=2, sort_keys=True)
    
    # return all HPO terms in the annotation, which is the result of set union
    # return set(reduce(lambda a, b: set(a) | set(b), [HPODesc['phenotypeList'] for HPODesc in gene2Phenotype.values()]))

def calcDisease2PhenotypeJson(tree):
    IOUtils.showInfo("Calculating disease to phenotype json.")
    disease2Phenotype = dict()
    with open(file=config.disease2PhenotypeAnnotationPath, mode='rt', encoding='utf-8') as fp:
        titleLineScanned = False
        for line in fp:
            if (not line.startswith("#")): # skip comments
                if (not titleLineScanned):   # skip title line
                    titleLineScanned = True
                else:
                    termsInLine = line.strip().split('\t')
                    if (len(termsInLine) >= 4):
                        diseaseId = termsInLine[0]
                        diseaseName = termsInLine[1]
                        phenotype = termsInLine[3]

                        if (disease2Phenotype.get(diseaseId) == None):
                            disease2Phenotype[diseaseId] = {
                                "name": set(),
                                "phenotypeList": set()
                            }
                        disease2Phenotype[diseaseId]["name"].add(diseaseName)
                        disease2Phenotype[diseaseId]["phenotypeList"].add(tree.getValidHPOTerm(phenotype))

            line = fp.readline()

    # check if one id has multiple names, and convert set to list
    for (key, value) in disease2Phenotype.items():
        value["name"] = list(value["name"])
        value["phenotypeList"] = list(value["phenotypeList"])
        if (len(value["name"]) > 1):
            IOUtils.showInfo(f"Disease '{key}' has multiple names: {value['name']}", 'WARN')
    
    with open(file=config.disease2PhenotypeJsonPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=disease2Phenotype, fp=fp, indent=2, sort_keys=True)

    with open(file=config.diseaseListPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=list(disease2Phenotype.keys()), fp=fp, indent=2, sort_keys=True)

    # return all HPO terms in the annotation, which is the result of set union
    # return set(reduce(lambda a, b: set(a) | set(b), [HPODesc['phenotypeList'] for HPODesc in disease2Phenotype.values()]))

# def loadHPOList():
#     HPOTree = HPOUtils.loadHPOTree()
#     HPOTermList = HPOTree.getHPOTermList()
#     with open(file=config.HPOListPath, mode='wt', encoding='utf-8') as fp:
#         json.dump(obj=HPOTermList, fp=fp, indent=2, sort_keys=True)


def calcTermICWithDisease(tree):
    IOUtils.showInfo("Calculating Disease IC.")
    # get HPO2Disease json
    with open(file=config.disease2PhenotypeJsonPath, mode='rt', encoding='utf-8') as fp:
        disease2HPO = json.load(fp)
    
    # with open(file=config.HPOListPath, mode='rt', encoding='utf-8') as fp:
        # HPOList = json.load(fp)

    with open(file=config.diseaseListPath, mode='rt', encoding='utf-8') as fp:
        diseaseList = json.load(fp)
    diseaseCount = len(diseaseList)
    
    # init with HPOList in case there is some HPO not show up in annotation
    HPO2Disease = {}
    for HPOTerm in tree.getValidHPOTermList():
        HPO2Disease[HPOTerm] = set()
    for (disease, diseaseDesc) in disease2HPO.items():
        for HPOTerm in diseaseDesc['phenotypeList']:
            currentNode = tree.getHPO(HPOTerm)
            HPO2Disease[currentNode.id].add(disease)
            for ancestor in currentNode.ancestors:
                HPO2Disease[ancestor].add(disease)

    # note: diseaseListForOneHPO may be empty if there is no annotation for this HPO term.
    diseaseIC = {HPO: (-math.log2(len(diseaseListForOneHPO) / diseaseCount)) if len(diseaseListForOneHPO) > 0 else 0
                  for (HPO, diseaseListForOneHPO) in HPO2Disease.items()}
    
    with open(file=config.ICFromDiseasePath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=diseaseIC, fp=fp, indent=2, sort_keys=True)
    
    return diseaseIC
    

def calcTermICWithGene(tree):
    IOUtils.showInfo("Calculating Gene IC.")
    with open(file=config.gene2PhenotypeJsonPath, mode='rt', encoding='utf-8') as fp:
        gene2HPO = json.load(fp)
    
    # with open(file=config.HPOListPath, mode='rt', encoding='utf-8') as fp:
        # HPOList = json.load(fp)

    with open(file=config.geneListPath, mode='rt', encoding='utf-8') as fp:
        geneList = json.load(fp)
    geneCount = len(geneList)
    
    # init with HPOList in case there is some HPO not show up in annotation
    HPO2Gene = {}
    for HPOTerm in tree.getValidHPOTermList():
        HPO2Gene[HPOTerm] = set()
    for (gene, geneDesc) in gene2HPO.items():
        for HPOTerm in geneDesc['phenotypeList']:
            currentNode = tree.getHPO(HPOTerm)
            HPO2Gene[currentNode.id].add(gene)
            for ancestor in currentNode.ancestors:
                HPO2Gene[ancestor].add(gene)

    # note: geneListForOneHPO may be empty if there is no annotation for this HPO term.
    geneIC = {HPO: (-math.log2(len(geneListForOneHPO) / geneCount)) if len(geneListForOneHPO) > 0 else 0
                  for (HPO, geneListForOneHPO) in HPO2Gene.items()}
    
    with open(file=config.ICFromGenePath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=geneIC, fp=fp, indent=2, sort_keys=True)

    return geneIC

def calcIntegratedIC(tree, diseaseIC, geneIC):
    IOUtils.showInfo("Calculating Integrated IC.")
    integratedIC = dict()

    for HPOTerm in tree.getValidHPOTermList():
        diseaseICForTerm = diseaseIC[HPOTerm]
        geneICForTerm = geneIC[HPOTerm]
        if (diseaseICForTerm == 0):
            integratedIC[HPOTerm] = geneICForTerm
        elif (geneICForTerm == 0):
            integratedIC[HPOTerm] = diseaseICForTerm
        else:
            integratedIC[HPOTerm] = math.sqrt(diseaseICForTerm * geneICForTerm)

    with open(file=config.integratedICPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=integratedIC, fp=fp, indent=2, sort_keys=True)
    
    return integratedIC

def calcSimilarity(tree):
    ancestorIndexsList = [node.ancestorIndexs for node in tree.HPOList.values()]

    IOUtils.showInfo("Calculating Similarity Matrix.")
    HPOCount = len(tree.getValidHPOTermList())
    ICList = tree.ICList
    ICArray = cupy.array(ICList)
    
    # CPU version
    MICAMatrix = numpy.zeros([HPOCount, HPOCount], dtype=numpy.float32)
    denominatorMatrx = ICArray[:, None] + ICArray[None, :]


    # version 1
    # items = tree.HPOList.items()
    # for (term1, node1) in items:
    #     index1 = node1.index
    #     node1AncestorIndexs = node1.ancestorIndexs
    #     for (term2, node2) in items:
    #         index2 = node2.index
    #         if (index1 == index2):
    #             # similarityMatrix[index1, index2] = 1
    #             MICAMatrix[index1, index2] = ICList[index1]
    #             break    # only calculate index2 in range of [0, index1], which is a triangle.
    #         else:
    #             commonAncestorIndexs= node1AncestorIndexs & node2.ancestorIndexs
    #             MICAMatrix[index1, index2] = max([ICList[ancestorIndex] for ancestorIndex in commonAncestorIndexs])
    

    # version 2
    for index1 in range(0, HPOCount):
        node1AncestorIndexs = ancestorIndexsList[index1]
        for index2 in range (0, index1):
            commonAncestorIndexs = node1AncestorIndexs & ancestorIndexsList[index2]
            MICAMatrix[index1, index2] = max([ICList[ancestorIndex] for ancestorIndex in commonAncestorIndexs])
                
    IOUtils.showInfo("MICA Calculation finished!")
    MICAMatrix = cupy.array(MICAMatrix) * 2
    similarityMatrix = cupy.divide(MICAMatrix, denominatorMatrx).get()
    IOUtils.showInfo("Similarity calc finished!")


    # CPU version of numpy
    # ICArray = numpy.array(tree.ICList, dtype=numpy.float32)
    # ancestorMaskMatrix = numpy.array([node.ancestorMask for node in tree.HPOList.values()])
    # ancestorMaskMatrixWithIC = numpy.multiply(ICArray, ancestorMaskMatrix)
    # for (term, node) in tree.HPOList.items():
    #     thisICArray = numpy.array([ICArray[node.index]] * HPOCount, dtype=numpy.float32)
    #     commonAncestorMaskMatrixWithIC = numpy.multiply(numpy.array(node.ancestorMask), ancestorMaskMatrixWithIC)
    #     MICAArrayWithIC = numpy.max(commonAncestorMaskMatrixWithIC, axis=1)
    #     numerator = MICAArrayWithIC * 2       # 2 * IC_MICA
    #     denominator = thisICArray + ICArray   # IC_Term1 + IC_Term2
    #     similarityForOneTerm = numpy.divide(numerator, denominator, out=numpy.zeros_like(numerator), where=denominator != 0)
    #     similarityMatrix[node.index, :] = similarityForOneTerm
    #     IOUtils.showInfo(f"{node.index}/{HPOCount}")

    # GPU version of cupy
    # ICArray = cupy.array(tree.ICList, dtype=cupy.float32)
    # ancestorIndexMatrix = [cupy.array(list(node.ancestorIndexs)) for node in tree.HPOList.values()]
    # # ancestorMaskMatrixWithIC = cupy.multiply(ICArray, ancestorMaskMatrix)
    # for (term, node) in tree.HPOList.items():
    #     # thisICArray = cupy.array([ICArray[node.index]] * HPOCount, dtype=cupy.float32)

    #     # IOUtils.showInfo("Step 1")
    #     ancestorIndexArray = cupy.array(list(node.ancestorIndexs))
    #     # commonAncestorMaskMatrixWithIC = cupy.multiply(ancestorMaskArray, ancestorMaskMatrixWithIC)
    #     commonAncestorIndex = cupy.array([cupy.intersect1d(ancestorIndexArray, cupy.array(row)) for row in ancestorIndexMatrix])
    #     commonAncestorIC = (ICArray[commonAncestorIndex])
    #     # commonAncestorMaskMatrixWithIC = cupy.where(ancestorMaskArray == 0, 0, ancestorMaskMatrixWithIC)

    #     # IOUtils.showInfo("Step 2")
    #     MICAArrayWithIC = cupy.max(commonAncestorIC, axis=1)

    #     # IOUtils.showInfo("Step 3")
    #     numerator = MICAArrayWithIC * 2       # 2 * IC_MICA

    #     # IOUtils.showInfo("Step 4")
    #     denominator = ICArray + ICArray[node.index]   # IC_Term1 + IC_Term2
        
    #     # IOUtils.showInfo("Step 5")
    #     similarityForOneTerm = cupy.where(denominator != 0, numerator/denominator, 0)

    #     # IOUtils.showInfo("Step 6")
    #     similarityMatrix[node.index, :] = cupy.asnumpy(similarityForOneTerm)

    #     # IOUtils.showInfo("Step 7")
    #     # if (node.index == 10):
    #         # break
    #     if (node.index % 100 == 0):
    #         IOUtils.showInfo(f"{node.index}/{HPOCount}")

    # numpy.savetxt('a.txt', similarityMatrix)




def main():
    IOUtils.showInfo("Start preprocessing...")
    tree = HPOUtils.loadHPOTree()
    calcGene2PhenotypeJson(tree)
    calcDisease2PhenotypeJson(tree)
    diseaseIC = calcTermICWithDisease(tree)
    geneIC = calcTermICWithGene(tree)
    integratedIC = calcIntegratedIC(tree, diseaseIC, geneIC)
    tree.setIC(integratedIC)
    calcSimilarity(tree)

    IOUtils.showInfo("Preprocess finished.")


if (__name__ == '__main__'):
    main()