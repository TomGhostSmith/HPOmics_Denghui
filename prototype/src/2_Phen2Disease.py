import sys
import os
import numpy
import json
sys.path.append(".")

import config.config as config
import utils.IOUtils as IOUtils
import utils.HPOUtils as HPOUtils
from model.Patient import Patient
from model.Disease import Disease
from model.Disease import DiseaseEvaluator
from model.Gene import Gene
from model.Gene import GeneEvaluator

def evaluate(HPOTree, diseaseEvaluator, geneEvaluator):
    patientFiles = os.listdir(config.patientPath)
    processedCount = 0
    totalCount = len(patientFiles)

    # start and end index can be modified to skip some patient
    startIndex = 0
    endIndex = len(patientFiles)

    for file in patientFiles:
        # check index to skip some patients do not need to process
        if (processedCount < startIndex or processedCount >= endIndex):
            processedCount += 1
            IOUtils.showInfo(f"[{processedCount}/{totalCount}] Skipped file {str(file)}")
            continue

        # extract file name
        dotIndex = str(file).rfind('.')
        if (dotIndex != -1):
            fileName = str(file)[:dotIndex]
        else:
            fileName = str(file)

        # extract HPO term and replace old term with new
        with open(file=f"{config.patientPath}/{file}", mode='rt', encoding='utf-8') as fp:
            HPOList, totalIC = extractPreciseHPONodes(HPOTree, fp.readlines())

        # can be modified to execute disease task and gene task customly
        patient = Patient(fileName=fileName, HPOList=HPOList, info=None, taskType=config.taskType, totalIC=totalIC)  # info can be used in the future

        # evaluate case
        if (patient.taskType == 'disease'):
            diseaseEvaluator.evaluate(patient)
        else:
            geneEvaluator.evaluate(patient)
        
        # store result
        with open(file=f'{config.splitResultPath}/{fileName}.csv', mode='wt', encoding='utf-8') as fp:
            fp.writelines(patient.getResult())
        
        processedCount += 1
        IOUtils.showInfo(f"[{processedCount}/{totalCount}] Processed file {str(file)}")

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

def initEvaluator(HPOTree):
    # load disease list and init disease evaluator
    diseaseList = list()
    with open(file=config.disease2PhenotypeJsonPath, mode='rt', encoding='utf-8') as fp:
        disease2PhenotypeJson = json.load(fp)
    for (id, disease) in disease2PhenotypeJson.items():
        relatedHPONodes, totalIC = extractPreciseHPONodes(HPOTree, disease['phenotypeList'])
        diseaseList.append(Disease(id, disease['name'], relatedHPONodes, totalIC))
    diseaseEvaluator = DiseaseEvaluator(diseaseList, HPOTree)

    # load gene list and init gene evaluator
    geneList = list()
    with open(file=config.gene2PhenotypeJsonPath, mode='rt', encoding='utf-8') as fp:
        gene2PhenotypeJson = json.load(fp)
    for (id, gene) in gene2PhenotypeJson.items():
        relatedHPONodes, totalIC = extractPreciseHPONodes(HPOTree, gene['phenotypeList'])
        geneList.append(Gene(id, gene['name'], relatedHPONodes, totalIC))
    geneEvaluator = GeneEvaluator(geneList, HPOTree)

    return diseaseEvaluator, geneEvaluator

def initEvaluatorFromPhenoBrain(HPOTree):
    # load disease list and init disease evaluator
    diseaseList = list()
    with open(file="./data/preprocess/disease2phenotype_phenobrain.json", mode='rt', encoding='utf-8') as fp:
        disease2PhenotypeJson = json.load(fp)
    for disease in disease2PhenotypeJson:
        relatedHPONodes, totalIC = extractPreciseHPONodes(HPOTree, disease[0])
        diseaseID = None
        for name in disease[1]:
            if (str(name).startswith('OMIM')):
                diseaseID = name
                break
        if (diseaseID == None):
            if (len(disease[1]) > 0):
                IOUtils.showInfo(f"{disease[1][0]} does not have an OMIM id")
                diseaseID = disease[1][0]
            else:
                diseaseID = ''
        diseaseList.append(Disease(diseaseID, '', relatedHPONodes, totalIC))
    diseaseEvaluator = DiseaseEvaluator(diseaseList, HPOTree)

    return diseaseEvaluator, None

def main():
    HPOTree = HPOUtils.loadHPOTree()
    HPOUtils.setIC(HPOTree)
    HPOUtils.setSimilarity(HPOTree)
    diseaseEvaluator, geneEvaluator = initEvaluator(HPOTree)
    # diseaseEvaluator, geneEvaluator = initEvaluatorFromPhenoBrain(HPOTree)
    IOUtils.showInfo("Start evaluate")
    evaluate(HPOTree, diseaseEvaluator, geneEvaluator)
    IOUtils.showInfo("Process finished")

if (__name__ == '__main__'):
    main()

    # a = {'a': 1, 'b': 1, 'c': 1, 'd': 1}
    # print('b' not in a.keys())
    # v = 1  # True, will insert this term
    # for (t, v) in a.items():
    #     if (t == 'b' or t == 'c'):
    #         a[t] = 0
    #     if (t == 'd'):
    #         v = 0  # false, will not insert this term
    # a['e'] = v
    # print(a)