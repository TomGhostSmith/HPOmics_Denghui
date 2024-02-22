from utils import IOUtils
from utils import HPOUtils
import config.config as config

class Gene:
    def __init__(self, id, name, relatedHPONodes, totalIC) -> None:
        self.id = id      # NCBI gene id
        self.name = name  # gene symbol, which can be a list
        self.relatedHPONodes = relatedHPONodes
        self.relatedDiseaseList = None
        self.totalIC = totalIC
    
    def getType(self):
        countMap = {geneType: 0 for geneType in config.HPOClasses.values()}
        for node in self.relatedHPONodes:
            HPOTypes = node.getType()
            for HPOType in HPOTypes:
                countMap[HPOType] += 1
        return sorted(countMap.items(), key=lambda pair:pair[1], reverse=True)[0][0]
    
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

class GeneEvaluator:
    def __init__(self, geneList, HPOTree):
        self.geneList = geneList.geneIDMap.values()
        self.HPOTree = HPOTree

    def evaluate(self, patient):
        scores = dict()

        for gene in self.geneList:
            gene2PatientScore = 0
            for geneNode in gene.relatedHPONodes:
                similarities = list()
                for patientNode in patient.HPOList:
                    similarities.append(self.HPOTree.getSimilarity(geneNode, patientNode, 'Lin'))
                similarities.append(0)
                thisIC = self.HPOTree.ICList[geneNode.index]
                gene2PatientScore += max(similarities) * thisIC

            patient2GeneScore = 0
            for patientNode in patient.HPOList:
                similarities = list()
                for geneNode in gene.relatedHPONodes:
                    similarities.append(self.HPOTree.getSimilarity(geneNode, patientNode, 'Lin'))
                similarities.append(0)
                thisIC = self.HPOTree.ICList[patientNode.index]
                patient2GeneScore += max(similarities) * thisIC

            if (gene.totalIC + patient.totalIC == 0):
                IOUtils.showInfo(f"No informative HPO for gene {gene.name} and patient {patient.fileName}")
            else:
                scores[gene] = f"{gene2PatientScore}, {patient2GeneScore}, {gene.totalIC}, {patient.totalIC}"
        
        patient.results = scores