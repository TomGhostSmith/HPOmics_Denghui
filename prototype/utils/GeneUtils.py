import json
import sys
sys.path.append('.')

from config import config
from model.Gene import Gene
from model.Gene import GeneList
from utils.HPOUtils import HPOUtils
import utils.IOUtils as IOUtils


class GeneUtil:
    def __init__(self) -> None:
        self.reset()
    
    def reset(self):
        if (config.autoLoadAnnotation):
            self.geneList = loadGenes()
        else:
            self.geneList = None

    def evaluate(self, patient):
        if (self.geneList == None):
            IOUtils.showInfo('Annotations not loaded. Please run preprocess.py and set config.autoLoadAnnotation to True', 'ERROR')
            exit()
        scores = dict()

        for gene in self.geneList.geneIDMap.values():
            gene2PatientScore = 0
            for geneNode in gene.relatedHPONodes:
                similarities = list()
                for patientNode in patient.HPOList:
                    similarities.append(HPOUtils.HPOTree.getSimilarity(geneNode, patientNode, config.similarityMethod))
                similarities.append(0)
                thisIC = HPOUtils.HPOTree.ICList[geneNode.index]
                gene2PatientScore += max(similarities) * thisIC

            patient2GeneScore = 0
            for patientNode in patient.HPOList:
                similarities = list()
                for geneNode in gene.relatedHPONodes:
                    similarities.append(HPOUtils.HPOTree.getSimilarity(geneNode, patientNode, config.similarityMethod))
                similarities.append(0)
                thisIC = HPOUtils.HPOTree.ICList[patientNode.index]
                patient2GeneScore += max(similarities) * thisIC

            if (gene.totalIC + patient.totalIC == 0):
                IOUtils.showInfo(f"No informative HPO for gene {gene.name} and patient {patient.fileName}")
            else:
                scores[gene] = f"{gene2PatientScore}, {patient2GeneScore}, {gene.totalIC}, {patient.totalIC}"
        
        patient.results = scores

def loadGenes():
    geneList = GeneList()
    with open(file=config.gene2PhenotypeJsonPath, mode='rt', encoding='utf-8') as fp:
        gene2PhenotypeJson = json.load(fp)
    for (id, gene) in gene2PhenotypeJson.items():
        relatedHPONodes, totalIC = HPOUtils.extractPreciseHPONodes(gene['phenotypeList'])
        geneType = gene['type']
        geneList.addGene(Gene(id, gene['name'], relatedHPONodes, totalIC, geneType))
    return geneList

GeneUtils = GeneUtil()