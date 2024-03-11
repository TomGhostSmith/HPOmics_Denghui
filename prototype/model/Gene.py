import multiprocessing
import sys
sys.path.append('.')

from utils import IOUtils
from utils.HPOUtils import HPOUtils
from config import config
import model.Patient as Patient

class Gene:
    def __init__(self, id, name, relatedHPONodes, totalIC, geneType, relatedDiseases) -> None:
        self.id = id      # NCBI gene id
        self.name = name  # gene symbol, which can be a list
        self.relatedHPONodes = relatedHPONodes   # a set of related HPO nodes
        self.relatedDiseases = relatedDiseases   # a list of related disease terms
        self.totalIC = totalIC
        self.type = geneType
    
class GeneList:
    def __init__(self) -> None:
        self.geneIDMap = dict()  # key: disease id, value: disease node
        self.geneSymbolMap = dict()  # key: disease id, value: disease node
        self.geneLink = None

    def addGene(self, gene):
        self.geneIDMap[gene.id] = gene
        for name in gene.name:
            self.geneSymbolMap[name] = gene
    
    def searchGeneByID(self, geneID):
        result = self.geneIDMap.get(geneID)
        if (result == None):
            IOUtils.showInfo(f'cannot find gene with id {geneID}', 'WARN')
        return result
    
    def searchGeneByName(self, geneName):
        result = self.geneSymbolMap.get(geneName)
        if (result == None):
            IOUtils.showInfo(f'cannot find gene with name {geneName}', 'WARN')
        return result
    
    # def searchGene(self, nameOrId):
    #     try:
    #         geneID = int(nameOrId)
    #         return self.searchGeneByID(geneID)
    #     except:
    #         geneName = nameOrId
    #         return self.searchGeneByName(geneName)

    def getRelatedGenes(self, gene):   # param gene should be a Gene object
        geneID = gene.id
        geneName = gene.name
        relatedGenes = self.geneLink.get(geneID)
        if (relatedGenes == None):
            relatedGenes = self.geneLink.get(geneName)
            if (relatedGenes == None):
                relatedGenes = dict()
        return relatedGenes