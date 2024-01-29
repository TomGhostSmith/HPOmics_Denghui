class Gene:
    def __init__(self, id, name, relatedHPOList) -> None:
        self.id = id      # NCBI gene id
        self.name = name  # gene symbol
        self.relatedHPOList = relatedHPOList  # a list of HPO id
        self.relatedDiseaseList = None
    
    def setRelatedDiseaseList(self, relatedDiseaseList):
        self.relatedDiseaseList = relatedDiseaseList