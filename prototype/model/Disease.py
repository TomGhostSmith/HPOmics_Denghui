import json
import sys
import math
sys.path.append(".")

import config.config as config
import utils.IOUtils as IOUtils
from model.Patient import Patient

class Disease:
    def __init__(self, id, name, relatedHPONodes, totalIC) -> None:
        self.id = id         # disease id, like OMIM:xxxxxx
        self.name = name     # disease name
        self.relatedHPONodes = relatedHPONodes
        self.relatedGeneList = None
        self.totalIC = totalIC
    
    # def setRelatedGeneList(self, relatedGeneList):
    #     self.relatedGeneList = relatedGeneList
        


class DiseaseEvaluator:
    def __init__(self, diseaseList, HPOTree) -> None:
        self.diseaseList = diseaseList
        self.HPOTree = HPOTree

    def evaluate(self, patient):
        scores = dict()

        for disease in self.diseaseList:
            # sim(patient, disease) = numerator / denominator, where
            # numerator = disease2patient part and patient2disease part
            # disease2patient part: for each term in disease, find most related term in patient with IC
            # patient2disease part: for each term in patient, find most related term in disease with IC
            # denominator: IC for all terms in disease or patient

            disease2PatientScore = 0
            for diseaseNode in disease.relatedHPONodes:
                similarities = list()
                for patientNode in patient.HPOList:
                    similarities.append(self.HPOTree.getSimilarity(diseaseNode, patientNode))
                similarities.append(0)
                thisIC = self.HPOTree.ICList[diseaseNode.index]
                disease2PatientScore += max(similarities) * thisIC
                # print(f"disease {diseaseNode.id}: ic = {thisIC}, maxSimilarity = {max(similarities)}, res = {max(similarities) * thisIC}")

                
        
            patient2DiseaseScore = 0
            for patientNode in patient.HPOList:
                similarities = list()
                for diseaseNode in disease.relatedHPONodes:
                    similarities.append(self.HPOTree.getSimilarity(diseaseNode, patientNode))
                similarities.append(0)
                thisIC = self.HPOTree.ICList[patientNode.index]
                patient2DiseaseScore += max(similarities) * thisIC
                # print(f"patient {patientNode.id}: ic = {thisIC}, maxSimilarity = {max(similarities)}, res = {max(similarities) * thisIC}")

            
            if (disease.totalIC + patient.totalIC == 0):
                IOUtils.showInfo(f'No informative HPO for disease {disease.id} and patient {patient.fileName}')
            else:
                # scores[disease] = (disease2PatientScore + patient2DiseaseScore) / (disease.totalIC + patient.totalIC)  # double
                # scores[disease] = (disease2PatientScore + patient2DiseaseScore) / (disease.totalIC + patient.totalIC) + patient2DiseaseScore / patient.totalIC  # double + p2d
                # scores[disease] = (disease2PatientScore + patient2DiseaseScore) / (disease.totalIC + patient.totalIC) * patient2DiseaseScore / patient.totalIC  # double * p2d
                # scores[disease] = patient2DiseaseScore / patient.totalIC  # p2d
                # if (disease.totalIC != 0):
                    # scores[disease] = (disease2PatientScore / disease.totalIC + patient2DiseaseScore / patient.totalIC)/2  # d2p + p2d
                # scores[disease] = math.sqrt((disease2PatientScore + patient2DiseaseScore) / (disease.totalIC + patient.totalIC) * patient2DiseaseScore / patient.totalIC)  # double * p2d
                # print(f"result for disease {disease.id}: {disease2PatientScore + patient2DiseaseScore} / {disease.totalIC + patient.totalIC} = {scores[disease]}")

                # for test only
                scores[disease] = f"{disease2PatientScore}, {patient2DiseaseScore}, {disease.totalIC}, {patient.totalIC}"
        # patient.results = dict(sorted(scores.items(), key=lambda pair : pair[1], reverse=True))
        patient.results = scores
        