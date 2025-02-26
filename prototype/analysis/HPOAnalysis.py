# import requests
import os
import json
import sys
sys.path.append('.')

from config import config
from utils import IOUtils
from utils.HPOUtils import HPOUtils
from utils.GeneUtils import GeneUtils
from utils.DiseaseUtils import DiseaseUtils


def getHPOTypeDistribution(HPOList):
    for HPONode in HPOList:
        for HPOType in HPONode.getType():
            HPOTypeDistribution[HPOType] += 1
    HPOTypeDistribution = {key:value for (key, value) in HPOTypeDistribution.items() if value > 0}
    HPOTypeDistribution = dict(sorted(HPOTypeDistribution.items(), key=lambda pair:pair[1], reverse=True))
    return HPOTypeDistribution

def getStandardResultType(standardResults):
    resultTypeDistribution = {HPOType: 0 for HPOType in config.HPOClasses.values()}
    for standardResult in standardResults:
        if (config.taskType == 'disease'):
            result = DiseaseUtils.diseaseList.searchDisease(standardResult)
        else:
            result = GeneUtils.geneList.searchGeneByName(standardResult)
        if (result != None):
            resultTypeDistribution[result.type] += 1
    resultTypeDistribution = {key:value for (key, value) in resultTypeDistribution.items() if value > 0}
    resultTypeDistribution = dict(sorted(resultTypeDistribution.items(), key=lambda pair:pair[1], reverse=True))

    return resultTypeDistribution

def checkOneDataset(dataset, taskType):
    config.datasetName = dataset
    config.taskType = taskType
    config.resetPath()
    IOUtils.init()
    IOUtils.showInfo(f'Start analysis HPO types and result types for dataset {config.testsetName}')

    patientFiles = os.listdir(config.patientPath)
    resultLines = list()
    resultLines.append("ID,HPO,HPOTypeDistribution,StandardResult,ResultType\n")

    IOUtils.showInfo('Start analysing')
    for file in patientFiles:
        # skip folders
        if (os.path.isdir(f"{config.patientPath}/{file}")):
            continue

        # check patient HPO type distribution
        HPOTypeDistribution = {HPOType: 0 for HPOType in config.HPOClasses.values()}
        with open(file=f"{config.patientPath}/{file}", mode='rt', encoding='utf-8') as fp:
            HPOTerms = [term.strip() for term in fp.readlines()]
        HPOList, totalIC = HPOUtils.extractPreciseHPONodes(HPOTerms)
        HPOTypeDistribution = getHPOTypeDistribution(HPOList)
        HPOTypeDistribution = str(HPOTypeDistribution).replace('"', '').replace("'", "").replace('{', '').replace('}', '').replace(',', ';')
        
        # check standard result type
        with open(f"{config.standardResultPath}/{file}") as fp:
            lines = fp.readlines()
        standardResults = [line.strip() for line in lines]
        resultTypeDistribution = getStandardResultType(standardResults)

        if (len(resultTypeDistribution.keys()) == 0):
            resultType = 'NIL'
        elif (len(resultTypeDistribution.keys()) == 1):
            resultType = list(resultTypeDistribution.keys())[0]
        else:
            resultType = str(resultTypeDistribution).replace('"', '').replace("'", "").replace('[', '').replace(']', '').replace(',', ';')

        
        HPOTerms = str(HPOTerms).replace('"', '').replace("'", "").replace('[', '').replace(']', '').replace(',', ';')
        standardResults = str(standardResults).replace('"', '').replace("'", "").replace('[', '').replace(']', '').replace(',', ';')
        resultLines.append(f"{file},{HPOTerms},{HPOTypeDistribution},{standardResults},{resultType}\n")
    
    with open(file=f"{config.analysisPath}/analysis_for_{config.testsetName}.csv", mode='wt', encoding='utf-8') as fp:
        fp.writelines(resultLines)
    
    IOUtils.showInfo('Done')

def main():
    checkOneDataset(dataset='data6', taskType='gene')

if (__name__ == '__main__'):
    main()