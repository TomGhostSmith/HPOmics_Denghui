import json
import sys
import math
sys.path.append(".")

from config import config
import utils.IOUtils as IOUtils
from utils.HPOUtils import HPOUtils
from model.Patient import Patient

class Disease:
    def __init__(self, id, name, relatedHPONodes, totalIC, diseaseType, relatedGenes) -> None:
        self.id = id         # disease id, like OMIM:xxxxxx
        self.name = name     # disease name
        self.relatedHPONodes = relatedHPONodes  # a set of related HPO nodes
        self.relatedGenes = relatedGenes
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
        self.synonym = dict()   # store some disease id which are not in the diseaseMap. use this dict to map them into exising diseases

    def addDisease(self, disease):
        self.diseaseMap[disease.id] = disease
    
    def searchDisease(self, diseaseID):
        synonym = self.synonym.get(diseaseID)
        if (synonym == None):
            return self.diseaseMap.get(diseaseID)
        else:
            return self.diseaseMap.get(synonym)
    
    def setSynonym(self, synonym):
        for (key, value) in synonym.items():
            if (isinstance(value, str)):  # ignore CCRD synonyms
                if (self.diseaseMap.get(value) == None and self.diseaseMap.get(key) != None):
                    self.synonym[value] = key