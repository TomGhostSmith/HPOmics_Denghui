import json
import sys
import math
sys.path.append(".")

from config import config
import utils.IOUtils as IOUtils
from utils.HPOUtils import HPOUtils
from model.Patient import Patient

class Disease:
    def __init__(self, id, name, relatedHPONodes, totalIC, diseaseType) -> None:
        self.id = id         # disease id, like OMIM:xxxxxx
        self.name = name     # disease name
        self.relatedHPONodes = relatedHPONodes
        self.relatedGeneList = None
        self.totalIC = totalIC
        self.type = diseaseType
    
    # def getType(self):
        # return self.type
        # countMap = {diseaseType: 0 for diseaseType in config.HPOClasses.values()}
        # for node in self.relatedHPONodes:
        #     HPOTypes = node.getType()
        #     for HPOType in HPOTypes:
        #         countMap[HPOType] += 1
        # return sorted(countMap.items(), key=lambda pair:pair[1], reverse=True)[0][0]

class DiseaseList:
    def __init__(self) -> None:
        self.diseaseMap = dict()  # key: disease id, value: disease node

    def addDisease(self, disease):
        self.diseaseMap[disease.id] = disease
    
    def searchDisease(self, diseaseID):
        return self.diseaseMap.get(diseaseID)

