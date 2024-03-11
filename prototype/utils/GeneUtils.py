import json
import sys
import numpy
sys.path.append('.')

from config import config
from model.Gene import Gene
from model.Gene import GeneList
from utils.HPOUtils import HPOUtils
import utils.IOUtils as IOUtils


class GeneUtil:
    def __init__(self) -> None:
        self.geneList = None
    
    def reset(self):
        self.geneList = loadGenes()
        with open(file=config.geneLinkPath, mode='rt', encoding='utf-8') as fp:
            self.geneList.geneLink = json.load(fp)
        IOUtils.showInfo('Gene link loaded')

    def evaluate(self, patient):
        if (self.geneList == None):
            IOUtils.showInfo('Annotations not loaded', 'ERROR')
            exit()
        scores = dict()

        for gene in self.geneList.geneIDMap.values():
            if (config.similarityMethod == 'phrank'):
                scores[gene] = evaluateWithPhrank(gene, patient)
            elif (config.similarityMethod == 'phenoBrain'):
                scores[gene] = evaluateWithPhenoBrain(gene, patient)
            else:
                scores[gene] = evaluateWithSimilarity(gene, patient)
        
        patient.geneResults = scores

def loadGenes():
    geneList = GeneList()
    with open(file=config.gene2PhenotypeJsonPath, mode='rt', encoding='utf-8') as fp:
        gene2PhenotypeJson = json.load(fp)
    with open(file=config.gene2DiseaseJsonPath, mode='rt', encoding='utf-8') as fp:
        gene2DiseaseJson = json.load(fp)
    for (id, gene) in gene2PhenotypeJson.items():
        if (config.useAncestor == 'target' or config.useAncestor == 'both'):
            HPOInput = gene['phenotypeList']
            totalIC = 0
            HPOList = set()
            for HPOTerm in HPOInput:
                validNode = HPOUtils.HPOTree.getHPO(HPOTerm.strip())
                if (validNode != None):
                    HPOList.add(validNode)
                    for ancestorIndex in validNode.ancestorIndexs:
                        HPOList.add(HPOUtils.HPOTree.nodes[ancestorIndex])
            for HPONode in HPOList:
                totalIC += HPOUtils.HPOTree.ICList[HPONode.index]
            relatedHPONodes = HPOList
        else:
            relatedHPONodes, totalIC = HPOUtils.extractPreciseHPONodes(gene['phenotypeList'])
        
        geneType = gene['type']
        geneNames = gene['name']
        relatedDiseases = set()
        for geneName in geneNames:
            relatedDiseasesForOneName = gene2DiseaseJson.get(geneName)
            if (relatedDiseasesForOneName != None):
                relatedDiseases |= set(relatedDiseasesForOneName)
        geneList.addGene(Gene(id, geneNames, relatedHPONodes, totalIC, geneType, list(relatedDiseases)))
    return geneList

def evaluateWithSimilarity(gene, patient):
    gene2PatientScore = 0
    for geneNode in gene.relatedHPONodes:
        similarities = list()
        for patientNode in patient.HPOList:
            similarities.append(HPOUtils.HPOTree.getSimilarity(geneNode, patientNode, config.similarityMethod))
        similarities.append(0)
        thisIC = HPOUtils.HPOTree.ICList[geneNode.index]
        # IOUtils.showInfo(f"g2p: {similarities} * {thisIC}")
        gene2PatientScore += max(similarities) * thisIC

    patient2GeneScore = 0
    for patientNode in patient.HPOList:
        similarities = list()
        for geneNode in gene.relatedHPONodes:
            similarities.append(HPOUtils.HPOTree.getSimilarity(geneNode, patientNode, config.similarityMethod))
        similarities.append(0)
        thisIC = HPOUtils.HPOTree.ICList[patientNode.index]
        # IOUtils.showInfo(f"p2g: {similarities} * {thisIC}")
        patient2GeneScore += max(similarities) * thisIC

    if (gene.totalIC + patient.totalIC == 0):
        IOUtils.showInfo(f"No informative HPO for gene {gene.name} and patient {patient.fileName}", 'WARN')
        return f"0,0,0,0"
    else:
        return f"{gene2PatientScore}, {patient2GeneScore}, {gene.totalIC}, {patient.totalIC}"

def evaluateWithPhrank(gene, patient):
    geneAncestorIndexs = set()
    patientAncestorIndexs = set()
    for node in gene.relatedHPONodes:
        geneAncestorIndexs |= node.ancestorIndexs  # include itself
    for node in patient.HPOList:
        patientAncestorIndexs |= node.ancestorIndexs   # include itself
    commonAncestorIndexs = geneAncestorIndexs & patientAncestorIndexs
    return sum([HPOUtils.HPOTree.ICList[idx] for idx in commonAncestorIndexs])

def evaluateWithPhenoBrain(gene, patient):
    geneAncestorIndexs = set()
    patientAncestorIndexs = set()
    geneIndexs = {node.index for node in gene.relatedHPONodes}
    patientIndexs = {node.index for node in patient.HPOList}
    for node in gene.relatedHPONodes:
        geneAncestorIndexs |= node.ancestorIndexs  # include itself
    for node in patient.HPOList:
        patientAncestorIndexs |= node.ancestorIndexs   # include itself
    
    patient2GeneCommonAncestorIndexs = patientIndexs & geneAncestorIndexs
    gene2PatientCommonAncestorIndexs = geneIndexs & patientAncestorIndexs

    patient2GeneScore = sum([HPOUtils.HPOTree.ICList[idx] for idx in patient2GeneCommonAncestorIndexs])
    gene2PatientScore = sum([HPOUtils.HPOTree.ICList[idx] for idx in gene2PatientCommonAncestorIndexs])

    if (gene.totalIC + patient.totalIC == 0):
        IOUtils.showInfo(f'No informative HPO for gene {gene.name} and patient {patient.fileName}', 'WARN')
        return "0,0,0,0"
    else:
        return f"{gene2PatientScore}, {patient2GeneScore}, {gene.totalIC}, {patient.totalIC}"

GeneUtils = GeneUtil()