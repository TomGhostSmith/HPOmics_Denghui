import sys
import os
import math
import json
sys.path.append('.')

from config import config
from utils import IOUtils
from utils.DiseaseUtils import DiseaseUtils
from utils.GeneUtils import GeneUtils

def calcGene(geneOriginScore, relatedDiseaseScores):
    # method 1: based on related disease scores
    if (len(relatedDiseaseScores) > 0):
        finalScore = max(relatedDiseaseScores)
    else:
        finalScore = 0
    
    # method 2: integrated with average
    # maxDiseaseProportion = 0.5
    # if (len(relatedDiseaseScores) > 0):
    #     diseaseProportion = (1 - 1/(1 + len(relatedDiseaseScores))) * maxDiseaseProportion
    #     finalScore = geneOriginScore * (1 - diseaseProportion) + sum(relatedDiseaseScores)/len(relatedDiseaseScores) * diseaseProportion
    # else:
    #     finalScore = geneOriginScore

    # method 3: integrated with max
    # maxDiseaseProportion = 0.5
    # if (len(relatedDiseaseScores) > 0):
    #     diseaseProportion = (1 - 1/(1 + len(relatedDiseaseScores))) * maxDiseaseProportion
    #     finalScore = geneOriginScore * (1 - diseaseProportion) + sum(relatedDiseaseScores)/len(relatedDiseaseScores) * diseaseProportion
    # else:
    #     finalScore = geneOriginScore

    return finalScore


def calcDisease(diseaseOriginScore, relatedGeneScores):
    return diseaseOriginScore

def calcPhenoBrain(disease2Patient, patient2Disease, diseaseIC, patientIC):
    return (disease2Patient + patient2Disease)/2
    # return patient2Disease

def calc(disease2Patient, patient2Disease, diseaseIC, patientIC):
    # return (disease2Patient + patient2Disease)/(diseaseIC + patientIC)
    if (patientIC != 0 and diseaseIC + patientIC != 0):
    # if (patientIC != 0):
        # return patient2Disease/patientIC
        return (disease2Patient + patient2Disease)/(diseaseIC + patientIC) + patient2Disease/patientIC
    # if (patientIC != 0):
        # return patient2Disease/patientIC
    else:
        return 0
    # return (disease2Patient + 4*patient2Disease)/(diseaseIC + 4*patientIC) + patient2Disease/patientIC
    # return patient2Disease/patientIC
    if (diseaseIC != 0):
        return (disease2Patient/diseaseIC + patient2Disease/patientIC)/2
        # return ((disease2Patient + patient2Disease)/(diseaseIC + patientIC))
    #     return (disease2Patient + patient2Disease)/(diseaseIC + patientIC) + disease2Patient/diseaseIC
    else:
        return patient2Disease/patientIC
        # return 0


    if (diseaseIC == 0):
        return 0
    elif (disease2Patient/diseaseIC > 0.25):
    # elif (diseaseIC > patientIC):
        return patient2Disease/patientIC
    else:
        return patient2Disease/patientIC * 0.95
        # return ((disease2Patient + patient2Disease)/(diseaseIC + patientIC) + patient2Disease/patientIC)/2
        # return (disease2Patient/diseaseIC + patient2Disease/patientIC)/2

        # return max(patient2Disease/patientIC, disease2Patient/diseaseIC)
        # return (patient2Disease/patientIC*diseaseIC + disease2Patient/diseaseIC*patientIC)/(patientIC + diseaseIC)

def combineFiles(files, diseaseSynonym):
    for file in files:
        # skip folders
        if (os.path.isdir(f"{config.splitResultPath}/{file}")):
            continue

        with open(f"{config.splitResultPath}/{file}") as fp:
            scores = fp.readlines()
        diseaseScores = dict()
        geneScores = dict()

        # load split result and combine for each gene/disease
        for line in scores:
            if (line.startswith('id')):
                continue
            terms = line.strip().split(',')
            if (config.similarityMethod == 'phrank'):
                res = float(terms[2])
            elif (config.similarityMethod == 'phenoBrain'):
                res = calcPhenoBrain(float(terms[2]), float(terms[3]), float(terms[4]), float(terms[5]))
            else:  # Lin, JC, IC
                res = calc(float(terms[2]), float(terms[3]), float(terms[4]), float(terms[5]))
            if (terms[1].strip() == ''):
                # disease
                diseaseScores[terms[0]] = res
            else:
                # gene
                geneScores[terms[1]] = res

        # link gene-disease for integrated prediction
        finalScores = dict()
        if (config.taskType == 'disease'):
            for (disease, diseaseScore) in diseaseScores.items():
                relatedGenes = DiseaseUtils.diseaseList.searchDisease(disease).relatedGenes
                relatedGeneText = ''
                relatedGeneScores = list()
                for gene in relatedGenes:
                    geneScore = geneScores.get(gene)
                    if (geneScore != None):
                        relatedGeneScores.append(geneScore)
                        relatedGeneText += f'{gene}:{geneScore}; '
                if (len(relatedGeneScores) > 0):
                    maxScore = max(relatedGeneScores)
                else:
                    maxScore = 0
                if (diseaseSynonym.get(disease) != None):
                    pass
                finalScores[disease] = (calcDisease(diseaseScore, relatedGeneScores), diseaseScore, relatedGeneText, max(relatedGeneScores))
        else:
            for (gene, geneScore) in geneScores.items():
                relatedDiseases = GeneUtils.geneList.searchGeneByName(gene).relatedDiseases
                relatedDiseaseScores = list()
                relatedDiseaseText = ''
                for disease in relatedDiseases:
                    diseaseScore = diseaseScores.get(disease)
                    if (diseaseScore != None):
                        relatedDiseaseScores.append(diseaseScore)
                        relatedDiseaseText += f'{disease}:{diseaseScore}; '
                if (len(relatedDiseaseScores) > 0):
                    maxScore = max(relatedDiseaseScores)
                else:
                    maxScore = 0
                finalScores[gene] = (calcGene(geneScore, relatedDiseaseScores), geneScore, relatedDiseaseText, maxScore)
        

        result = dict(sorted(finalScores.items(), key=lambda pair : pair[1], reverse=True))
        if (config.taskType == 'disease'):
            lines = [f'{key},,{value[0]},{value[1]},{value[2]},{value[3]}\n' for (key, value) in result.items()]
        else:
            lines = [f',{key},{value[0]},{value[1]},{value[2]},{value[3]}\n' for (key, value) in result.items()]
        lines.insert(0, 'id,name,finalScore,originScore,relatedScore,maxRelatedScore\n')
        with open(f"{config.resultPath}/{file}", 'wt') as fp:
            fp.writelines(lines)

def main():
    IOUtils.showInfo("Start combining splitted results")
    files = sorted(os.listdir(config.splitResultPath))

    with open(file=config.diseaseSynonymPath, mode='rt', encoding='utf-8') as fp:
        diseaseSynonym = json.load(fp)

    if (config.supportFork):
        caseCountForOne = math.ceil(len(files) / config.CPUCores)
        childPIDList = list()

        for i in range (config.CPUCores):
            pid = os.fork()
            if (pid == 0):
                startIndex = i * caseCountForOne
                endIndex = min((i + 1) * caseCountForOne, len(files))   # this index is not included
                combineFiles(files[startIndex:endIndex], diseaseSynonym)
                os._exit(0)
            else:
                IOUtils.showInfo(f'Forked subprocess with pid {pid}', 'PROC')
                childPIDList.append(pid)
        
        for pid in childPIDList:
            os.waitpid(pid, 0)
    else:
        combineFiles(files, diseaseSynonym)

    IOUtils.showInfo("Combination finished")
    
if (__name__ == '__main__'):
    main()