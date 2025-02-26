import sys
import os
import math
import json
import importlib
sys.path.append('.')

from config import config
from utils import IOUtils
from utils.HPOUtils import HPOUtils
from utils.DiseaseUtils import DiseaseUtils
from utils.GeneUtils import GeneUtils
from model.PPI import ppi

Phen2Disease = importlib.import_module('src.4_Phen2Disease')

def calcDisease2Gene(geneOriginScore, relatedDiseaseScores):
    if (config.disease2GeneProportionMethod == 'none'):
        return geneOriginScore
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

def calcGene2Disease(diseaseOriginScore, relatedGeneScores):
    # return diseaseOriginScore
    if (config.gene2DiseaseProportionMethod == 'none'):
        return diseaseOriginScore
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
        ratio = CADDScore * (1 - config.CADDMinValue) + config.CADDMinValue
        return originScore * ratio
    elif (config.CADDMethod == 'fixed'):
        return CADDScore * config.CADDMAxProportion + (1 - config.CADDMAxProportion) * originScore


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

def combineFiles(files, diseaseSynonym):
    allGeneList = set(GeneUtils.geneList.geneSymbolMap.keys()) | set(GeneUtils.geneList.geneLink.keys())

    for file in files:
        # skip folders
        if (os.path.isdir(f"{config.splitResultPath}/{file}")):
            continue

        if (config.CADDMethod != 'none' and os.path.exists(f"{config.CADDOutputFolder}/{file.replace('.csv', '.json')}")):
            with open(f"{config.CADDOutputFolder}/{file.replace('.csv', '.json')}") as fp:
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
        

        if (config.usePPI == 'broadcast'):
            # Note: actually, there are no "direct" genes! all are indirect!
            linkedGeneScores = dict()

            for gene in allGeneList:
                geneNodeID = ppi.nodeIndexMap.get(gene)
                if (geneNodeID != None):
                    totalScore = 0
                    totalWeight = 0
                    for relatedGene, pathLength in (zip(ppi.nodeIndexMap.keys(), ppi.cachedShortestPath[geneNodeID])):
                        thisGeneScore = geneScores.get(relatedGene)
                        if (thisGeneScore != None and pathLength != 0):
                            weight = 1 / pathLength
                            totalScore += weight * thisGeneScore
                            totalWeight += weight
                    indirectScore = totalScore / totalWeight if totalWeight > 0 else None

                selfScore = geneScores.get(gene)
                summedScore = 0
                summedWeight = 0
                if (selfScore != None):
                    summedScore += (config.selfProportion * selfScore)
                    summedWeight += config.selfProportion
                if (indirectScore != None):
                    summedScore += (config.indirectProportion * indirectScore)
                    summedWeight += config.indirectProportion
                
                if (summedWeight > 0):
                    linkedGeneScores[gene] = summedScore / summedWeight
            
            geneScores = linkedGeneScores


        elif (config.usePPI == True):
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

        # link gene-disease for integrated prediction
        finalScores = dict()
        if (config.taskType == 'disease'):
            for (disease, diseaseScore) in diseaseScores.items():
                diseaseObject = DiseaseUtils.diseaseList.searchDisease(disease)
                relatedGenes = diseaseObject.relatedGenes
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
        

        outputScores = dict()
        for key, value in finalScores.items():
            outputScores[key] = value[0]

        # with open(f"/Data/HPOmicsData/result/{config.datasetName}/Phen2Disease2/{file[:-4]}.json", 'wt') as fp:
        #     json.dump(outputScores, fp, indent=2, sort_keys=True)

        result = dict(sorted(finalScores.items(), key=lambda pair : pair[1], reverse=True))

        lines = getOutputResultLines(file[:-4], result)

        with open(f"{config.resultPath}/{file}", 'wt') as fp:
            fp.writelines(lines)
        


        
        # IOUtils.showInfo(f'combined {file}')

def calcHPOOverlap(patientHPONodes, targetHPONodes):  # return: HPO Terms
    targetHPOIndexs = {node.index for node in targetHPONodes}

    overlappedTargetHPOIndexs = set()
    overlappedPatientHPOIndexs = set()
    remainedPatientHPOIndexs = set()
    for patientHPONode in patientHPONodes:
        overLapAncestors = patientHPONode.ancestorIndexs & targetHPOIndexs
        if (len(overLapAncestors) > 0):
            overlappedTargetHPOIndexs |= overLapAncestors
            overlappedPatientHPOIndexs.add(patientHPONode.index)
        else:
            remainedPatientHPOIndexs.add(patientHPONode.index)
    
    remainedTargetHPOIndexs = targetHPOIndexs - overlappedTargetHPOIndexs

    overLapHPOIndexs = sorted(overlappedTargetHPOIndexs, key=lambda obj : HPOUtils.HPOTree.ICList[obj])
    excessHPOIndexs = sorted(remainedPatientHPOIndexs, key=lambda obj : HPOUtils.HPOTree.ICList[obj])
    lossHPOIndexs = sorted(remainedTargetHPOIndexs, key=lambda obj : HPOUtils.HPOTree.ICList[obj])

    overlapHPOs = [HPOUtils.HPOTree.nodes[index].id for index in overLapHPOIndexs]
    excessHPOs = [HPOUtils.HPOTree.nodes[index].id for index in excessHPOIndexs]
    lossHPOs = [HPOUtils.HPOTree.nodes[index].id for index in lossHPOIndexs]

    return overlapHPOs, excessHPOs, lossHPOs
            

def getOutputResultLines(fileName, result):  # filename should have no extension
    if (config.HPOmcisOutput):
        if (config.inputType == 'plain'):
            filePath = f'{config.patientPath}/{fileName}'
        elif (config.inputType == 'json'):
            filePath = f'{config.patientPath}/{fileName}.json'
        HPOList, totalIC, VCFFileName = Phen2Disease.loadPatient(fileName, filePath)
        
        lines = list()
        lines.append('id,name,finalScore,overlapHPO,excessHPO,lossHPO\n')
        if (config.taskType == 'disease'):
            for (key, value) in result.items():
                diseaseObject = DiseaseUtils.diseaseList.searchDisease(key)
                diseaseID = key
                if (diseaseObject != None):
                    overlapHPO, excessHPO, lossHPO = calcHPOOverlap(HPOList, diseaseObject.relatedHPONodes)
                    diseaseName = diseaseObject.name[0].replace(",", " ")
                else:
                    overlapHPO = []
                    excessHPO = []
                    lossHPO = []
                    diseaseName = ''
                lines.append(f'{diseaseID},{diseaseName},{value[0]},{";".join(overlapHPO)},{";".join(excessHPO)},{";".join(lossHPO)}\n')
        else:
            for (key, value) in result.items():
                geneObject = GeneUtils.geneList.searchGeneByName(key)
                geneName = key
                if (geneObject != None):
                    overlapHPO, excessHPO, lossHPO = calcHPOOverlap(HPOList, geneObject.relatedHPONodes)
                    geneID = geneObject.id
                else:
                    overlapHPO = []
                    excessHPO = []
                    lossHPO = []
                    geneID = ''
                lines.append(f'{geneID},{geneName},{value[0]},{";".join(overlapHPO)},{";".join(excessHPO)},{";".join(lossHPO)}\n')
    else:
        if (config.taskType == 'disease'):
            lines = [f'{key},,{value[0]},{value[1]},{value[2]},{value[3]}\n' for (key, value) in result.items()]
        else:
            lines = [f',{key},{value[0]},{value[1]},{value[2]},{value[3]}\n' for (key, value) in result.items()]
        lines.insert(0, 'id,name,finalScore,originScore,relatedScore,maxRelatedScore\n')
    return lines

def main():
    IOUtils.init(5)
    ppi.loadCache()
    HPOUtils.loadIC()
    GeneUtils.reset()
    DiseaseUtils.reset()
    IOUtils.showInfo("Start combining splitted results")
    files = sorted(os.listdir(config.splitResultPath))

    with open(file=config.diseaseSynonymPath, mode='rt', encoding='utf-8') as fp:
        diseaseSynonym = json.load(fp)

    # IOUtils.showInfo("Save result to /Data")
    # if (not os.path.exists(f"/Data/HPOmicsData/result/{config.datasetName}/Phen2Disease2")):
    #     os.makedirs(f"/Data/HPOmicsData/result/{config.datasetName}/Phen2Disease2")

    if (config.supportFork):
        caseCountForOne = math.ceil(len(files) / config.CPUCores)
        childPIDList = list()

        for i in range (config.CPUCores):
            pid = os.fork()
            if (pid == 0):
                startIndex = i * caseCountForOne
                endIndex = min((i + 1) * caseCountForOne, len(files))   # this index is not included
                combineFiles(files[startIndex:endIndex], diseaseSynonym)
                IOUtils.showInfo("Exit thread")
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

