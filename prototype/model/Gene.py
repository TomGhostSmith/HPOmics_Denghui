class Gene:
    def __init__(self, id, name, relatedHPONodes, totalIC) -> None:
        self.id = id      # NCBI gene id
        self.name = name  # gene symbol
        self.relatedHPONodes = relatedHPONodes  # a list of HPO id
        self.relatedDiseaseList = None
        self.totalIC = totalIC
    
    def setRelatedDiseaseList(self, relatedDiseaseList):
        self.relatedDiseaseList = relatedDiseaseList

class GeneEvaluator:
    def __init__(self, geneList, HPOTree):
        pass

    def evaluate(self, patient):
        pass