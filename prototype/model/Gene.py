import multiprocessing
import sys
sys.path.append('.')

from utils import IOUtils
from utils.HPOUtils import HPOUtils
from config import config
import model.Patient as Patient

class Gene:
    def __init__(self, id, name, relatedHPONodes, totalIC, geneType) -> None:
        self.id = id      # NCBI gene id
        self.name = name  # gene symbol, which can be a list
        self.relatedHPONodes = relatedHPONodes
        self.relatedDiseaseList = None
        self.totalIC = totalIC
        self.type = geneType
    
class GeneList:
    def __init__(self) -> None:
        self.geneIDMap = dict()  # key: disease id, value: disease node
        self.geneSymbolMap = dict()  # key: disease id, value: disease node

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