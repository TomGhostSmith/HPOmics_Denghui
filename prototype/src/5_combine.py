import sys
import os
import math
import json
sys.path.append('.')

from config import config
from utils import IOUtils
from utils.HPOUtils import HPOUtils
from utils.DiseaseUtils import DiseaseUtils
from utils.GeneUtils import GeneUtils

def calcDisease2Gene(geneOriginScore, relatedDiseaseScores):

    if (len(relatedDiseaseScores) > 0):
        # get integrated related disease score
        if (config.disease2GeneMethod == 'average'):
            relatedDiseaseSumScore = sum(relatedDiseaseScores)/len(relatedDiseaseScores)
        elif (config.disease2GeneMethod == 'max'):
            relatedDiseaseSumScore = max(relatedDiseaseScores)

        # integrate disease score with gene score
        if (config.disease2GeneProportionMethod == 'fixed'):
            finalScore = config.maxDiseaseProportion * relatedDiseaseSumScore + (1 - config.maxDiseaseProportion) * geneOriginScore
        elif (config.disease2GeneProportionMethod == 'float'):
            diseaseProportion = (1 - 1/(1 + len(relatedDiseaseScores))) * config.maxDiseaseProportion
            finalScore = diseaseProportion * relatedDiseaseSumScore + (1 - diseaseProportion) * geneOriginScore
    else:
        finalScore = geneOriginScore

    return finalScore

    # method 1: based on related disease scores
    # if (len(relatedDiseaseScores) > 0):
    #     finalScore = max(relatedDiseaseScores)
    # else:
    #     # finalScore = geneOriginScore
    #     finalScore = 0
    
    # method 2: integrated with average
    # maxDiseaseProportion = 0.5
    # if (len(relatedDiseaseScores) > 0):
    #     diseaseProportion = (1 - 1/(1 + len(relatedDiseaseScores))) * maxDiseaseProportion
    #     finalScore = geneOriginScore * (1 - diseaseProportion) + sum(relatedDiseaseScores)/len(relatedDiseaseScores) * diseaseProportion
    # else:
    #     finalScore = geneOriginScore

    # method 3: integrated with max
    # maxDiseaseProportion = config.maxDiseaseProportion
    # if (len(relatedDiseaseScores) > 0):
    #     diseaseProportion = (1 - 1/(1 + len(relatedDiseaseScores))) * maxDiseaseProportion
    #     finalScore = geneOriginScore * (1 - diseaseProportion) + max(relatedDiseaseScores) * diseaseProportion
    # else:
    #     finalScore = geneOriginScore



def calcGene2Disease(diseaseOriginScore, relatedGeneScores):
    # return diseaseOriginScore
    if (len(relatedGeneScores) > 0):
        # get integrated related gene score
        if (config.gene2DiseaseMethod == 'average'):
            relatedGeneSumScore = sum(relatedGeneScores)/len(relatedGeneScores)
        elif (config.gene2DiseaseMethod == 'max'):
            relatedGeneSumScore = max(relatedGeneScores)
            
        # integrate gene score with disease score
        if (config.gene2DiseaseProportionMethod == 'fixed'):
            finalScore = config.maxGeneProportion * relatedGeneSumScore + (1 - config.maxGeneProportion) * diseaseOriginScore
        elif (config.gene2DiseaseProportionMethod == 'float'):
            geneProportion = (1 - 1/(1 + len(relatedGeneScores))) * config.maxGeneProportion
            finalScore = geneProportion * relatedGeneSumScore + (1 - geneProportion) * diseaseOriginScore
    else:
        finalScore = diseaseOriginScore
    
    return finalScore

def mergeScoreWithCADD(originScore, CADDScore):
    if (config.CADDMethod == 'none'):
        return originScore
    elif (config.CADDMethod == 'multiply'):
        ratio = CADDScore * (1 - config.CADDMinRatio) + config.CADDMinRatio
        return originScore * ratio


def calcPhenoBrain(disease2Patient, patient2Disease, diseaseIC, patientIC):
    return (disease2Patient + patient2Disease)/2
    # return patient2Disease

# here, dg means disease or gene, which is set in config.taskType
def calc(dg2Patient, patient2DG, dgIC, patientIC):
    potentialScores = list()
    if ('double' in config.scoreCombineMethods and dgIC + patientIC != 0):
        potentialScores.append((dg2Patient + patient2DG) / (dgIC + patientIC))
    if ('p2dg' in config.scoreCombineMethods and patientIC != 0):
        potentialScores.append(patient2DG / patientIC)
    if ('dg2p' in config.scoreCombineMethods and dgIC != 0):
        potentialScores.append(dg2Patient / dgIC)
    
    if (len(potentialScores) > 0):
        finalScore = sum(potentialScores) / len(potentialScores)
    else:
        finalScore = 0

    return finalScore


    # # return (disease2Patient + patient2Disease)/(diseaseIC + patientIC)
    # if (patientIC != 0 and diseaseIC + patientIC != 0):
    # # if (patientIC != 0):
    #     # return patient2Disease/patientIC
    #     return ((disease2Patient + patient2Disease)/(diseaseIC + patientIC) + patient2Disease/patientIC)/2
    # # if (patientIC != 0):
    #     # return patient2Disease/patientIC
    # else:
    #     return 0
    # # return (disease2Patient + 4*patient2Disease)/(diseaseIC + 4*patientIC) + patient2Disease/patientIC
    # # return patient2Disease/patientIC
    # if (diseaseIC != 0):
    #     return (disease2Patient/diseaseIC + patient2Disease/patientIC)/2
    #     # return ((disease2Patient + patient2Disease)/(diseaseIC + patientIC))
    # #     return (disease2Patient + patient2Disease)/(diseaseIC + patientIC) + disease2Patient/diseaseIC
    # else:
    #     return patient2Disease/patientIC
    #     # return 0

    # if (diseaseIC == 0):
    #     return 0
    # elif (disease2Patient/diseaseIC > 0.25):
    # # elif (diseaseIC > patientIC):
    #     return patient2Disease/patientIC
    # else:
    #     return patient2Disease/patientIC * 0.95
    # return ((disease2Patient + patient2Disease)/(diseaseIC + patientIC) + patient2Disease/patientIC)/2
    # return (disease2Patient/diseaseIC + patient2Disease/patientIC)/2

    # return max(patient2Disease/patientIC, disease2Patient/diseaseIC)
    # return (patient2Disease/patientIC*diseaseIC + disease2Patient/diseaseIC*patientIC)/(patientIC + diseaseIC)

def combineFiles(files, diseaseSynonym):
    allGeneList = set(GeneUtils.geneList.geneSymbolMap.keys()) | set(GeneUtils.geneList.geneLink.keys())
    for file in files:
        # skip folders
        if (os.path.isdir(f"{config.splitResultPath}/{file}")):
            continue

        if (config.CADDMethod != 'none' and os.path.exists(f"{config.CADDOutputFolder}/{file}.json")):
            with open(f"{config.CADDOutputFolder}/{file}.json") as fp:
                CADDScores = json.load(fp)
            CADDmax = max(CADDScores.values())
            CADDmin = min(CADDScores.values())
            CADDdiffer = CADDmax - CADDmin
        else:
            CADDScores = dict()
            

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
                CADDScore = CADDScores.get(terms[1])
                if (CADDScore != None):
                    res = mergeScoreWithCADD(res, (CADDScore - CADDmin) / CADDdiffer)
            if (terms[1].strip() == ''):
                # this result is a disease
                diseaseScores[terms[0]] = res
            else:
                # this result is a gene
                geneScores[terms[1]] = res
        

        if (config.usePPI):
            # calc gene-gene related scores with ppi
            linkedGeneScores = dict()

            for gene in allGeneList:
                indirectRelatedGeneScores = dict()
                directRelatedGeneScores = list()

                currentGeneScore = geneScores.get(gene)  # may be none
                relatedGeneWeights = GeneUtils.geneList.geneLink.get(gene) # may be none
                totalWeight = 0
                if (relatedGeneWeights != None):
                    for (relatedGene, weight) in relatedGeneWeights.items():
                        relatedGeneScore = geneScores.get(relatedGene)  # may be none
                        if (relatedGeneScore != None):
                            if (weight != -1):
                                indirectRelatedGeneScores[relatedGene] = (weight, relatedGeneScore)
                                totalWeight += weight
                            else:
                                directRelatedGeneScores.append(relatedGeneScore)

                # add self to direct
                if (currentGeneScore != None):
                    directRelatedGeneScores.append(currentGeneScore)

                selfScore = currentGeneScore
                if (config.directScoreMethod == 'average'):
                    directScore = sum(directRelatedGeneScores) / len(directRelatedGeneScores) if len(directRelatedGeneScores) > 0 else None
                elif (config.directScoreMethod == 'max'):
                    directScore = max(directRelatedGeneScores) if len(directRelatedGeneScores) > 0 else None
                else:
                    directScore = None
                indirectScore = sum(weight * score for (weight, score) in indirectRelatedGeneScores.values()) / totalWeight if totalWeight > 0 else None

                summedScore = 0
                summedWeight = 0
                if (selfScore != None):
                    summedScore += selfScore * config.selfProportion
                    summedWeight += config.selfProportion
                if (directScore != None):
                    summedScore += directScore * config.directProportion
                    summedWeight += config.directProportion
                if (indirectScore != None):
                    summedScore += indirectScore * config.indirectProportion
                    summedWeight += config.indirectProportion
                
                if (summedWeight > 0):
                    linkedGeneScores[gene] = summedScore / summedWeight
                else:
                    linkedGeneScores[gene] = 0

            geneScores = linkedGeneScores

                # if (currentGeneScore != None):
                #     # method 0: if there is current score, then use current score
                #     linkedGeneScores[gene] = currentGeneScore
                # elif (len(directRelatedGeneScores) > 0):
                #     # method 1: if there is direct related gene, then use average score in direct related gene scores
                #     linkedGeneScores[gene] =
                # elif (totalWeight > 0):
                #     # method 2: if there is no direct related gene, use weighted average score of indirect genes
                #     weightedSumScore = 
                #     linkedGeneScores[gene] = weightedSumScore / totalWeight
                # else:
                #     linkedGeneScores[gene] = 0 

        

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
                integratedScore = (calcGene2Disease(diseaseScore, relatedGeneScores), diseaseScore, relatedGeneText, maxScore)
                synonyms = diseaseSynonym.get(disease)
                if (disease == 'ORPHA:25'):
                    print("?")
                if (synonyms != None):
                    if (isinstance(synonyms, str)):
                        synonyms = [synonyms]
                    for synonym in synonyms:
                        originScore = finalScores.get(synonym)
                        if (originScore == None or originScore[0] < integratedScore[0]):
                            finalScores[synonym] = integratedScore
                else:
                    originScore = finalScores.get(disease)
                    if (originScore == None or originScore[0] < integratedScore[0]):
                        finalScores[disease] = integratedScore

        else:
            for (gene, geneScore) in geneScores.items():
                geneObject = GeneUtils.geneList.searchGeneByName(gene)
                if (geneObject != None):
                    relatedDiseases = geneObject.relatedDiseases
                else:
                    relatedDiseases = list()
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
                finalScores[gene] = (calcDisease2Gene(geneScore, relatedDiseaseScores), geneScore, relatedDiseaseText, maxScore)
        

        result = dict(sorted(finalScores.items(), key=lambda pair : pair[1], reverse=True))
        if (config.taskType == 'disease'):
            lines = [f'{key},,{value[0]},{value[1]},{value[2]},{value[3]}\n' for (key, value) in result.items()]
        else:
            lines = [f',{key},{value[0]},{value[1]},{value[2]},{value[3]}\n' for (key, value) in result.items()]
        lines.insert(0, 'id,name,finalScore,originScore,relatedScore,maxRelatedScore\n')
        with open(f"{config.resultPath}/{file}", 'wt') as fp:
            fp.writelines(lines)

        
        # IOUtils.showInfo(f'combined {file}')

def main():
    IOUtils.init(5)
    HPOUtils.loadIC()
    GeneUtils.reset()
    DiseaseUtils.reset()
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

