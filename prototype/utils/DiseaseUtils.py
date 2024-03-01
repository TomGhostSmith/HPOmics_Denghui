import json
import sys
sys.path.append('.')

from config import config
from model.Disease import Disease
from model.Disease import DiseaseList
from utils.HPOUtils import HPOUtils
import utils.IOUtils as IOUtils

class DiseaseUtil:
    def __init__(self) -> None:
        self.diseaseList = None
        self.reset()
    
    def reset(self):
        if (config.autoLoadAnnotation):
            self.diseaseList = loadDiseases()

    def evaluate(self, patient):
        if (self.diseaseList == None):
            IOUtils.showInfo('Annotations not loaded. Please run preprocess.py and set config.autoLoadAnnotation to True', 'ERROR')
            exit()
        scores = dict()

        for disease in self.diseaseList.diseaseMap.values():
            if (config.similarityMethod == 'phrank'):
                scores[disease] = evaluateWithPhrank(disease, patient)
            elif (config.similarityMethod == 'phenoBrain'):
                scores[disease] = evaluateWithPhenoBrain(disease, patient)
            else:
                scores[disease] = evaluateWithSimilarity(disease, patient)
        patient.diseaseResults = scores

def loadDiseases():
    diseaseList = DiseaseList()
    with open(file=config.disease2PhenotypeJsonPath, mode='rt', encoding='utf-8') as fp:
        disease2PhenotypeJson = json.load(fp)
    with open(file=config.disease2GeneJsonPath, mode='rt', encoding='utf-8') as fp:
        disease2GeneJson = json.load(fp)
    for (id, disease) in disease2PhenotypeJson.items():
        # relatedHPONodes, totalIC = HPOUtils.extractPreciseHPONodes(disease['phenotypeList'])

        # test: use all ancestor node for disease
        HPOInput = disease['phenotypeList']
        totalIC = 0
        HPOList = set()
        HPONodes = list(HPOUtils.HPOTree.HPOList.values())
        for HPOTerm in HPOInput:
            validNode = HPOUtils.HPOTree.getHPO(HPOTerm.strip())
            if (validNode != None):
                HPOList.add(validNode)
                for ancestorIndex in validNode.ancestorIndexs:
                    HPOList.add(HPONodes[ancestorIndex])
        for HPONode in HPOList:
            totalIC += HPOUtils.HPOTree.ICList[HPONode.index]
        relatedHPONodes = HPOList
        
        diseaseType = disease['type']
        relatedGenes = disease2GeneJson.get(id)
        if (relatedGenes == None):
            relatedGenes = list()
        diseaseList.addDisease(Disease(id, disease['name'], relatedHPONodes, totalIC, diseaseType, relatedGenes))
    return diseaseList

def evaluateWithSimilarity(disease, patient):
    '''
    sim(patient, disease) = numerator / denominator, where
    numerator = disease2patient part and patient2disease part
    disease2patient part: for each term in disease, find most related term in patient with IC
    patient2disease part: for each term in patient, find most related term in disease with IC
    denominator: IC for all terms in disease or patient
    '''

    # if (disease.id in config.focusDisease):
    #     IOUtils.showInfo(f"Focus on disease {disease.id}:")
    #     IOUtils.showInfo(f"  + disease HPOs:")

    disease2PatientScore = 0
    for diseaseNode in disease.relatedHPONodes:
        similarities = list()
        for patientNode in patient.HPOList:
            similarities.append(HPOUtils.HPOTree.getSimilarity(diseaseNode, patientNode, config.similarityMethod))
        similarities.append(0)
        thisIC = HPOUtils.HPOTree.ICList[diseaseNode.index]
        disease2PatientScore += max(similarities) * thisIC
        # if (disease.id in config.focusDisease):
        #     IOUtils.showInfo(f"    - {diseaseNode.id}: ic = {thisIC:.3f}, maxSimilarity = {max(similarities):.3f}, res = {(max(similarities) * thisIC):.3f}")

    # if (disease.id in config.focusDisease):
    #     IOUtils.showInfo(f"    * disease2patient: {disease2PatientScore:.3f}, disease IC = {disease.totalIC:.3f}, sim = {(disease2PatientScore/disease.totalIC):.3f}")
    #     IOUtils.showInfo(f"  + patient HPOs:")        

    patient2DiseaseScore = 0
    for patientNode in patient.HPOList:
        similarities = list()
        for diseaseNode in disease.relatedHPONodes:
            similarities.append(HPOUtils.HPOTree.getSimilarity(diseaseNode, patientNode, config.similarityMethod))
        similarities.append(0)
        thisIC = HPOUtils.HPOTree.ICList[patientNode.index]
        patient2DiseaseScore += max(similarities) * thisIC
        # if (disease.id in config.focusDisease):
        #     IOUtils.showInfo(f"    - {patientNode.id}: ic = {thisIC:.3f}, maxSimilarity = {max(similarities):.3f}, res = {(max(similarities) * thisIC):.3f}")

    # if (disease.id in config.focusDisease):
    #     IOUtils.showInfo(f"    * patient2disease: {patient2DiseaseScore:.3f}, patient IC = {patient.totalIC:.3f}, sim = {(patient2DiseaseScore/patient.totalIC):.3f}")

    if (disease.totalIC + patient.totalIC == 0):
        IOUtils.showInfo(f'No informative HPO for disease {disease.id} and patient {patient.fileName}', 'WARN')
        return "0,0,0,0"
    else:
        return f"{disease2PatientScore}, {patient2DiseaseScore}, {disease.totalIC}, {patient.totalIC}"

def evaluateWithPhrank(disease, patient):
    diseaseAncestorIndexs = set()
    patientAncestorIndexs = set()
    for node in disease.relatedHPONodes:
        diseaseAncestorIndexs |= node.ancestorIndexs  # include itself
    for node in patient.HPOList:
        patientAncestorIndexs |= node.ancestorIndexs   # include itself
    commonAncestorIndexs = diseaseAncestorIndexs & patientAncestorIndexs
    return sum([HPOUtils.HPOTree.ICList[idx] for idx in commonAncestorIndexs])

def evaluateWithPhenoBrain(disease, patient):
    diseaseAncestorIndexs = set()
    patientAncestorIndexs = set()
    diseaseIndexs = {node.index for node in disease.relatedHPONodes}
    patientIndexs = {node.index for node in patient.HPOList}
    for node in disease.relatedHPONodes:
        diseaseAncestorIndexs |= node.ancestorIndexs  # include itself
    for node in patient.HPOList:
        patientAncestorIndexs |= node.ancestorIndexs   # include itself
    
    patient2DiseaseCommonAncestorIndexs = patientIndexs & diseaseAncestorIndexs
    disease2PatientCommonAncestorIndexs = diseaseIndexs & patientAncestorIndexs

    patient2DiseaseScore = sum([HPOUtils.HPOTree.ICList[idx] for idx in patient2DiseaseCommonAncestorIndexs])
    disease2PatientScore = sum([HPOUtils.HPOTree.ICList[idx] for idx in disease2PatientCommonAncestorIndexs])

    if (disease.totalIC + patient.totalIC == 0):
        IOUtils.showInfo(f'No informative HPO for disease {disease.id} and patient {patient.fileName}', 'WARN')
        return "0,0,0,0"
    else:
        return f"{disease2PatientScore}, {patient2DiseaseScore}, {disease.totalIC}, {patient.totalIC}"

DiseaseUtils = DiseaseUtil()