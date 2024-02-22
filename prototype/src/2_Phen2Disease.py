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
    # endIndex = 1
    endIndex = len(patientFiles)

    for file in patientFiles:
        # skip folders
        if (os.path.isdir(f"{config.patientPath}/{file}")):
            processedCount += 1
            IOUtils.showInfo(f"[{processedCount}/{totalCount}] Skipped folder {str(file)}")
            continue

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
            HPOList, totalIC = HPOUtils.extractPreciseHPONodes(HPOTree, fp.readlines())


            # test: use all ancestors
            # HPOInput = fp.readlines()
            # totalIC = 0
            # HPOList = set()
            # HPONodes = list(HPOTree.HPOList.values())
            # for HPOTerm in HPOInput:
            #     validNode = HPOTree.getHPO(HPOTerm.strip())
            #     if (validNode != None):
            #         HPOList.add(validNode)
            #         for ancestorIndex in validNode.ancestorIndexs:
            #             HPOList.add(HPONodes[ancestorIndex])
            # for HPONode in HPOList:
            #     totalIC += HPOTree.ICList[HPONode.index]
        

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

def main():
    IOUtils.init()
    IOUtils.showInfo(f"Start to evaluate dataset {config.testsetName}. Rank target: {config.taskType}")
    HPOTree = HPOUtils.loadHPOTree()
    HPOUtils.loadIC(HPOTree)
    HPOUtils.loadSimilarity(HPOTree)
    diseaseEvaluator = DiseaseEvaluator(HPOUtils.loadDiseases(HPOTree), HPOTree)
    geneEvaluator = GeneEvaluator(HPOUtils.loadGenes(HPOTree), HPOTree)
    IOUtils.showInfo("Start evaluate")
    evaluate(HPOTree, diseaseEvaluator, geneEvaluator)
    IOUtils.showInfo("Process finished")

if (__name__ == '__main__'):
    main()