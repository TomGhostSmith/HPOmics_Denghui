class Disease:
    def __init__(self, id, name, relatedHPOList) -> None:
        self.id = id         # disease id, like OMIM:xxxxxx
        self.name = name     # disease name
        self.relatedHPOList = relatedHPOList   # a list of HPO id
        self.relatedGeneList = None
    
    def setRelatedGeneList(self, relatedGeneList):
        self.relatedGeneList = relatedGeneList