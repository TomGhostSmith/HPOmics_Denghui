class Patient:
    def __init__(self, fileName, HPOList, info, taskType, totalIC):
        self.fileName = fileName
        self.HPOList = HPOList
        self.info = info
        self.diseaseResults = None
        self.geneResults = None
        # self.CADDScores = None
        self.taskType = taskType
        self.totalIC = totalIC
    
    # output result in lines
    def getResult(self):
        result = list()
        result.append('id, name, disease2Patient, patient2Disease, diseaseIC, patientIC,CADDScore\n')
        # CADDmax = max(self.CADDScores.values())
        # CADDmin = min(self.CADDScores.values())
        # CADDdiffer = CADDmax - CADDmin
        for (disease, score) in self.diseaseResults.items():
            # result.append(f'{disease.id}, {str(disease.name).replace(",", " ")}, {score}\n')
            result.append(f'{disease.id},,{score}\n')
        for (gene, score) in self.geneResults.items():
            result.append(f'{gene.id},{str(gene.name[0]).replace(",", " ")},{score}\n')
            # CADDScore = self.CADDScores.get(gene.name[0])
            # if (CADDScore != None):
            #     result.append(f'{gene.id},{str(gene.name[0]).replace(",", " ")},{score},{(CADDScore - CADDmin) / CADDdiffer}\n')
            # else:
            #     result.append(f'{gene.id},{str(gene.name[0]).replace(",", " ")},{score},0\n')

        return result