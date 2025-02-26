# run it when dataset modified
import sys
import json
import math
import numpy
import gzip
import os
from scipy.sparse import csr_matrix
# import cupy
sys.path.append(".")

from config import config
import utils.IOUtils as IOUtils
from utils.HPOUtils import HPOUtils
from model.HPO import HPO
from model.HPO import HPOTree
from model.Disease import Disease
from model.Gene import Gene


def calcLocalIC():
    IOUtils.showInfo("Calculating Local IC.")
    if (config.taskType == 'disease'):
        # get HPO2Disease json
        with open(file=config.disease2PhenotypeJsonPath, mode='rt', encoding='utf-8') as fp:
            disease2HPO = json.load(fp)

        with open(file=config.diseaseListPath, mode='rt', encoding='utf-8') as fp:
            diseaseList = json.load(fp)
        diseaseCount = len(diseaseList)
        
        # init with HPOList in case there is some HPO not show up in annotation
        HPO2Disease = {HPOTerm: (set(), set()) for HPOTerm in HPOUtils.HPOTree.getValidHPOTermList() }
        for (disease, diseaseDesc) in disease2HPO.items():
            for HPOTerm in diseaseDesc['phenotypeList']:
                currentNode = HPOUtils.HPOTree.getHPO(HPOTerm)
                HPO2Disease[currentNode.id][0].add(disease)
                for ancestor in currentNode.ancestors:
                    HPO2Disease[ancestor][0].add(disease)

        localDiseaseCount = 0        
        files = os.listdir(config.patientPath)
        for file in files:
            if (os.path.isdir(f"{config.patientPath}/{file}")):
                IOUtils.showInfo(f"Skipped folder {str(file)}", 'PROC')
                continue
            localDiseaseCount += 1
            with open(file=f"{config.patientPath}/{file}", mode='rt', encoding='utf-8') as fp:
                if (config.inputType == 'plain'):
                    HPOInput = fp.readlines()
                elif (config.inputType == 'json'):
                    patientInfo = json.load(fp)
                    HPOInput = patientInfo['HPOList']
            for HPOTerm in HPOInput:
                validNode = HPOUtils.HPOTree.getHPO(HPOTerm.strip())
                if (validNode != None):
                    HPO2Disease[validNode.id][1].add(file)
                    for ancestor in validNode.ancestors:
                        HPO2Disease[ancestor][1].add(file)

        localIC = {HPO: (-math.log2(((1 - config.localProportion) * len(diseaseListForOneHPO[0]) 
                    + config.localProportion * len(diseaseListForOneHPO[1]))
                / ((1 - config.localProportion) * diseaseCount 
                    + config.localProportion * localDiseaseCount)))
            if (1 - config.localProportion) * len(diseaseListForOneHPO[0]) + config.localProportion * len(diseaseListForOneHPO[1]) > 0 else 0
            for (HPO, diseaseListForOneHPO) in HPO2Disease.items()}

    else:
        # calculate with gene
        with open(file=config.gene2PhenotypeJsonPath, mode='rt', encoding='utf-8') as fp:
            gene2HPO = json.load(fp)

        with open(file=config.geneListPath, mode='rt', encoding='utf-8') as fp:
            geneList = json.load(fp)
        geneCount = len(geneList)
        
        # init with HPOList in case there is some HPO not show up in annotation
        HPO2Gene = {HPOTerm: (set(), set()) for HPOTerm in HPOUtils.HPOTree.getValidHPOTermList()}

        for (gene, geneDesc) in gene2HPO.items():
            for HPOTerm in geneDesc['phenotypeList']:
                currentNode = HPOUtils.HPOTree.getHPO(HPOTerm)
                HPO2Gene[currentNode.id][0].add(gene)
                for ancestor in currentNode.ancestors:
                    HPO2Gene[ancestor][0].add(gene)

        files = os.listdir(config.patientPath)
        localGeneCount = 0
        for file in files:
            if (os.path.isdir(f"{config.patientPath}/{file}")):
                IOUtils.showInfo(f"Skipped folder {str(file)}", 'PROC')
                continue
            localGeneCount += 1
            with open(file=f"{config.patientPath}/{file}", mode='rt', encoding='utf-8') as fp:
                HPOInput = fp.readlines()
            for HPOTerm in HPOInput:
                validNode = HPOUtils.HPOTree.getHPO(HPOTerm.strip())
                if (validNode != None):
                    HPO2Gene[validNode.id][1].add(file)
                    for ancestor in validNode.ancestors:
                        HPO2Gene[ancestor][1].add(file)

        # localIC = dict()
        # for (HPO, geneListForOneHPO) in HPO2Gene.items():
        #     upper = (1 - config.localProportion) * len(geneListForOneHPO[0]) + config.localProportion * len(geneListForOneHPO[1])
        #     down = (1 - config.localProportion) * geneCount + config.localProportion * localGeneCount
        #     if (len(geneListForOneHPO[0]) + len(geneListForOneHPO[1]) > 0):
        #         localIC[HPO] = -math.log2(upper / down)
        #     else:
        #         localIC[HPO] = 0

        localIC = {HPO: (-math.log2(((1 - config.localProportion) * len(geneListForOneHPO[0]) 
                    + config.localProportion * len(geneListForOneHPO[1]))
                / ((1 - config.localProportion) * geneCount 
                    + config.localProportion * localGeneCount))) 
            if (1 - config.localProportion) * len(geneListForOneHPO[0]) + config.localProportion * len(geneListForOneHPO[1]) > 0 else 0
            for (HPO, geneListForOneHPO) in HPO2Gene.items()}
        
    with open(file=config.localICPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=localIC, fp=fp, indent=2, sort_keys=True)


def main():
    IOUtils.init(2)
    config.ICType = 'local'
    config.resetPath()
    calcLocalIC()

if (__name__ == '__main__'):
    main()