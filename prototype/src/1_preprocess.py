# program should run under root folder of the project
import sys
import json
import math
import numpy
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

if (config.GPUAvailable):
    import cupy

def calcSynonymDisease():
    diseaseSynonymMap = dict()

    # load ORPHA to OMIM map
    with open(file=config.diseaseSynonymAnnotationPath, mode='rt', encoding='utf-8') as fp:
        synonyms = json.load(fp)
    synonyms = synonyms['JDBOR'][0]["DisorderList"][0]["Disorder"]
    for synonym in synonyms:
        orphanCode = f"ORPHA:{synonym['OrphaCode']}"
        refs = synonym["ExternalReferenceList"][0].get('ExternalReference')
        if (refs != None):
            for ref in refs:
                if (ref['Source'] == 'OMIM'):
                    OMIMCode = f"OMIM:{ref['Reference']}"
                    diseaseSynonymMap[orphanCode] = OMIMCode
    
    # load CCRD to ORPHA or OMIM map
    with open(file=config.phenoBrainCCRD2ORPHAPath, mode='rt', encoding='utf-8') as fp:
        synonyms = json.load(fp)
    for (CCRDTerm, values) in synonyms.items():
        diseaseSynonymMap[CCRDTerm] = list()
        for group in values:
            ORPHATerm = group[0]
            OMIMTerm = diseaseSynonymMap.get(ORPHATerm)
            if (OMIMTerm == None):
                diseaseSynonymMap[CCRDTerm].append(ORPHATerm)
            else:
                diseaseSynonymMap[CCRDTerm].append(OMIMTerm)
    
    with open(file=config.diseaseSynonymPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=diseaseSynonymMap, fp=fp, indent=2, sort_keys=True)

def calcGeneDiseaseMapJson():
    IOUtils.showInfo('Calculating gene - disease mapping json')
    gene2Disease = dict()
    disease2Gene = dict()
    with open(file=config.gene2DiseaseAnnotationPath, mode='rt', encoding='utf-8') as fp:
        fp.readline()  # skip the first line (title line)

        line = fp.readline()
        while (line):
            termsInLine = line.strip().split('\t')
            if (len(termsInLine) > 3):
                geneSymbol = termsInLine[1]
                diseaseID = termsInLine[3]

                if (geneSymbol != '-' and diseaseID != '-'):  # add map only when gene and disease are both known
                    if (gene2Disease.get(geneSymbol) == None):
                        gene2Disease[geneSymbol] = set()
                    if (disease2Gene.get(diseaseID) == None):
                        disease2Gene[diseaseID] = set()
                    
                    gene2Disease[geneSymbol].add(diseaseID)
                    disease2Gene[diseaseID].add(geneSymbol)
            
            line = fp.readline()
    
    for (key, value) in gene2Disease.items():
        gene2Disease[key] = list(value)
    
    for (key, value) in disease2Gene.items():
        disease2Gene[key] = list(value)
    
    with open(file=config.gene2DiseaseJsonPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=gene2Disease, fp=fp, indent=2, sort_keys=True)
    
    with open(file=config.disease2GeneJsonPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=disease2Gene, fp=fp, indent=2, sort_keys=True)

def calcGene2PhenotypeJson():
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
                gene2Phenotype[geneId]["phenotypeList"].add(HPOUtils.HPOTree.getValidHPOTerm(phenotype))

            line = fp.readline()

    # check if one id has multiple names, and convert set to list
    # calculate gene type
    for (key, value) in gene2Phenotype.items():
        value["name"] = list(value["name"])
        value["phenotypeList"] = list(value["phenotypeList"])
        if (len(value["name"]) > 1):
            IOUtils.showInfo(f"Gene ID '{key}' has multiple symbols: {value['name']}", 'WARN')
        
        for term in value["phenotypeList"]:
            countMap = {geneType: 0 for geneType in config.HPOClasses.values()}
            node = HPOUtils.HPOTree.getHPO(term)
            HPOTypes = node.getType()
            for HPOType in HPOTypes:
                countMap[HPOType] += 1
        value["type"] = sorted(countMap.items(), key=lambda pair:pair[1], reverse=True)[0][0]

        
    with open(file=config.gene2PhenotypeJsonPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=gene2Phenotype, fp=fp, indent=2, sort_keys=True)

    with open(file=config.geneListPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=list(gene2Phenotype.keys()), fp=fp, indent=2, sort_keys=True)
    


def calcDisease2PhenotypeJson():
    # test: ignore synonyms

    
    IOUtils.showInfo("Calculating disease to phenotype json.")
    disease2Phenotype = dict()
    # operating HPO annotation from OMIM
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

                        # test: replace ORPHA disease with OMIM. This might influence prediction of gene, so discard this test
                        # if (diseaseId.startswith('ORPHA')):
                        #     OMIMId = diseaseSynonymMap.get(diseaseId)
                        #     if (OMIMId != None):
                        #         diseaseId = OMIMId
                        #     # else:
                        #         # IOUtils.showInfo(f"Cannot find OMIM code for {diseaseId}")
                        diseaseName = termsInLine[1]
                        phenotype = termsInLine[3]

                        if (disease2Phenotype.get(diseaseId) == None):
                            disease2Phenotype[diseaseId] = {
                                "name": set(),
                                "phenotypeList": set()
                            }
                        validTerm = HPOUtils.HPOTree.getValidHPOTerm(phenotype)
                        disease2Phenotype[diseaseId]["name"].add(diseaseName)
                        if (validTerm != None):
                            disease2Phenotype[diseaseId]["phenotypeList"].add(validTerm)

    # operate HPO annotation from PhenoBrain using CCRD data
    # note: there might be some invalid HPO term in the annotation
    # with open(file=config.phenoBrainCCRD2HPOPath, mode='rt', encoding='utf-8') as fp:
    #     CCRDAnnotation = json.load(fp)
    # for (CCRDTerm, value) in CCRDAnnotation.items():
    #     OMIMTerms = diseaseSynonymMap.get(CCRDTerm)
    #     for OMIMTerm in OMIMTerms:
    #         if (disease2Phenotype.get(OMIMTerm) == None):
    #             disease2Phenotype[OMIMTerm] = {
    #                 "name": set(),
    #                 "phenotypeList": set()
    #             }
    #         for term in value['PHENOTYPE_LIST']:
    #             validTerm = tree.getValidHPOTerm(term)
    #             if (validTerm != None):
    #                 disease2Phenotype[OMIMTerm]['phenotypeList'].add(validTerm)
    
    # check if one id has multiple names, and convert set to list
    for (key, value) in disease2Phenotype.items():
        value["name"] = list(value["name"])
        value["phenotypeList"] = list(value["phenotypeList"])
        if (len(value["name"]) > 1):
            IOUtils.showInfo(f"Disease '{key}' has multiple names: {value['name']}", 'WARN')
            
        for term in value["phenotypeList"]:
            countMap = {geneType: 0 for geneType in config.HPOClasses.values()}
            node = HPOUtils.HPOTree.getHPO(term)
            HPOTypes = node.getType()
            for HPOType in HPOTypes:
                countMap[HPOType] += 1
        value["type"] = sorted(countMap.items(), key=lambda pair:pair[1], reverse=True)[0][0]

    with open(file=config.disease2PhenotypeJsonPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=disease2Phenotype, fp=fp, indent=2, sort_keys=True)

    with open(file=config.diseaseListPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=list(disease2Phenotype.keys()), fp=fp, indent=2, sort_keys=True)

def calcTermICWithDisease():
    IOUtils.showInfo("Calculating Disease IC.")
    # get HPO2Disease json
    with open(file=config.disease2PhenotypeJsonPath, mode='rt', encoding='utf-8') as fp:
        disease2HPO = json.load(fp)

    with open(file=config.diseaseListPath, mode='rt', encoding='utf-8') as fp:
        diseaseList = json.load(fp)
    diseaseCount = len(diseaseList)
    
    # init with HPOList in case there is some HPO not show up in annotation
    HPO2Disease = {HPOTerm: set() for HPOTerm in HPOUtils.HPOTree.getValidHPOTermList() }
    for (disease, diseaseDesc) in disease2HPO.items():
        for HPOTerm in diseaseDesc['phenotypeList']:
            currentNode = HPOUtils.HPOTree.getHPO(HPOTerm)
            HPO2Disease[currentNode.id].add(disease)
            for ancestor in currentNode.ancestors:
                HPO2Disease[ancestor].add(disease)

    # note: diseaseListForOneHPO may be empty if there is no annotation for this HPO term.
    diseaseIC = {HPO: (-math.log2(len(diseaseListForOneHPO) / diseaseCount)) if len(diseaseListForOneHPO) > 0 else 0
                  for (HPO, diseaseListForOneHPO) in HPO2Disease.items()}

    phrankDiseaseIC = dict()
    for HPONode in HPOUtils.HPOTree.HPOList.values():
        parentRelatedDiseases = set()
        for parentTerm in HPONode.parents:
            parentRelatedDiseases |= HPO2Disease[parentTerm]
        diseaseCountForOne = len(HPO2Disease[HPONode.id])
        if (HPONode.id == config.HPORoot):
            phrankDiseaseIC[HPONode.id] = 0
        else:
            phrankDiseaseIC[HPONode.id] = -math.log2(diseaseCountForOne/len(parentRelatedDiseases)) if diseaseCountForOne > 0 else 0

    
    with open(file=config.diseaseICPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=diseaseIC, fp=fp, indent=2, sort_keys=True)
    
    with open(file=config.phrankDiseaseICPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=phrankDiseaseIC, fp=fp, indent=2, sort_keys=True)
    
    return diseaseIC, phrankDiseaseIC
    

def calcTermICWithGene():
    IOUtils.showInfo("Calculating Gene IC.")
    with open(file=config.gene2PhenotypeJsonPath, mode='rt', encoding='utf-8') as fp:
        gene2HPO = json.load(fp)

    with open(file=config.geneListPath, mode='rt', encoding='utf-8') as fp:
        geneList = json.load(fp)
    geneCount = len(geneList)
    
    # init with HPOList in case there is some HPO not show up in annotation
    HPO2Gene = {}
    for HPOTerm in HPOUtils.HPOTree.getValidHPOTermList():
        HPO2Gene[HPOTerm] = set()
    for (gene, geneDesc) in gene2HPO.items():
        for HPOTerm in geneDesc['phenotypeList']:
            currentNode = HPOUtils.HPOTree.getHPO(HPOTerm)
            HPO2Gene[currentNode.id].add(gene)
            for ancestor in currentNode.ancestors:
                HPO2Gene[ancestor].add(gene)

    # note: geneListForOneHPO may be empty if there is no annotation for this HPO term.
    geneIC = {HPO: (-math.log2(len(geneListForOneHPO) / geneCount)) if len(geneListForOneHPO) > 0 else 0
                  for (HPO, geneListForOneHPO) in HPO2Gene.items()}
    

    phrankGeneIC = dict()
    for HPONode in HPOUtils.HPOTree.HPOList.values():
        parentRelatedGenes = set()
        for parentTerm in HPONode.parents:
            parentRelatedGenes |= HPO2Gene[parentTerm]
        geneCountForOne = len(HPO2Gene[HPONode.id])
        if (HPONode.id == config.HPORoot):
            phrankGeneIC[HPONode.id] = 0
        else:
            phrankGeneIC[HPONode.id] = -math.log2(geneCountForOne/len(parentRelatedGenes)) if geneCountForOne > 0 else 0

    
    with open(file=config.geneICPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=geneIC, fp=fp, indent=2, sort_keys=True)

    with open(file=config.phrankGeneICPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=phrankGeneIC, fp=fp, indent=2, sort_keys=True)

    return geneIC, phrankGeneIC

def calcIntegratedIC(diseaseIC, geneIC):
    IOUtils.showInfo("Calculating Integrated IC.")
    integratedIC = dict()

    for HPOTerm in HPOUtils.HPOTree.getValidHPOTermList():
        diseaseICForTerm = diseaseIC[HPOTerm]
        geneICForTerm = geneIC[HPOTerm]
        if (diseaseICForTerm == 0):
            integratedIC[HPOTerm] = geneICForTerm
        elif (geneICForTerm == 0):
            integratedIC[HPOTerm] = diseaseICForTerm
        else:
            integratedIC[HPOTerm] = (diseaseICForTerm + geneICForTerm)/2
    
    return integratedIC

def calcMICAMatrix():
    ancestorIndexsList = [node.ancestorIndexs for node in HPOUtils.HPOTree.HPOList.values()]

    IOUtils.showInfo("Calculating MICA Matrix")
    HPOCount = len(HPOUtils.HPOTree.getValidHPOTermList())
    ICList = HPOUtils.HPOTree.ICList
    
    MICAMatrix = numpy.zeros([HPOCount, HPOCount], dtype=numpy.float32)

    # calculate MICA Matrix, only lower triangle
    for index1 in range(0, HPOCount):
        node1AncestorIndexs = ancestorIndexsList[index1]
        for index2 in range (0, index1):
            commonAncestorIndexs = node1AncestorIndexs & ancestorIndexsList[index2]
            MICAMatrix[index1, index2] = max([ICList[ancestorIndex] for ancestorIndex in commonAncestorIndexs])
    IOUtils.showInfo("MICA Matrix calc finished, saving result")
    numpy.savez_compressed(config.MICAMatirxPath, MICAMatrix=MICAMatrix)
    IOUtils.showInfo("MICA Matrix saved")


def main():
    calcSynonymDisease()
    IOUtils.showInfo("Start preprocessing...")
    calcGeneDiseaseMapJson()
    calcGene2PhenotypeJson()
    calcDisease2PhenotypeJson()
    diseaseIC, phrankDiseaseIC = calcTermICWithDisease()
    geneIC, phrankGeneIC = calcTermICWithGene()
    integratedIC = calcIntegratedIC(diseaseIC, geneIC)
    with open(file=config.integratedICPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=integratedIC, fp=fp, indent=2, sort_keys=True)
    phrankIntegratedIC = calcIntegratedIC(phrankDiseaseIC, phrankGeneIC)
    with open(file=config.phrankIntegratedICPath, mode='wt', encoding='utf-8') as fp:
        json.dump(obj=phrankIntegratedIC, fp=fp, indent=2, sort_keys=True)
    if (config.ICType == 'disease'):
        HPOUtils.HPOTree.setIC(diseaseIC)
    elif (config.ICType == 'gene'):
        HPOUtils.HPOTree.setIC(geneIC)
    elif (config.ICType == 'integrated'):
        HPOUtils.HPOTree.setIC(integratedIC)
    elif (config.ICType == 'phrankDisease'):
        HPOUtils.HPOTree.setIC(phrankDiseaseIC)
    elif (config.ICType == 'phrankGene'):
        HPOUtils.HPOTree.setIC(phrankGeneIC)
    elif (config.ICType == 'phrankIntegrated'):
        HPOUtils.HPOTree.setIC(phrankIntegratedIC)
    else:
        IOUtils.showInfo(f'Invalid IC type: {config.ICType}', 'ERROR')
        exit()
    calcMICAMatrix()

    IOUtils.showInfo("Preprocess finished.")


if (__name__ == '__main__'):
    # main()
    calcSynonymDisease()